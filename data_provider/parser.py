#!/usr/bin/env python
''' Get emails, parse them and pass to API '''

import json
import threading
import time
from datetime import datetime
from email.parser import BytesParser
from email.policy import default
from imaplib import IMAP4_SSL

import msgpack
import requests
import zmq

from imap_credentials import (imap_password, imap_port, imap_server,
                              imap_username)

URL = 'http://127.0.0.1:5000/api'


def parse_email(raw_emails):
    ''' parse email '''
    emails = list()

    for uid, length, raw_email in raw_emails:
        email_dict = dict()
        email = BytesParser(policy=default).parsebytes(raw_email)
        email['uid'] = uid.decode()
        email['lenth'] = length.decode()
        email_dict['Date'] = datetime.strptime(
            email['Date'], '%a, %d %b %Y %H:%M:%S %z')
        email_dict['metadata'] = dict()

        for header in ['From', 'To', 'Delivered-To',
                       'Message-ID', 'Subject']:
            email_dict['metadata'][header] = email[header]
        email_dict['plain'] = None
        email_dict['html'] = None
        email_dict['attachments'] = list()

        for part in email.walk():
            if not part.get('Content-Disposition'):
                if part.get_content_type() == 'text/html':
                    email_dict['html'] = part.get_body().get_content()
                elif part.get_content_type() == 'text/plain':
                    email_dict['plain'] = part.get_body().get_content()
            else:
                attachment = dict()
                attachment['MIME'] = part.get_content_type()
                attachment['filename'] = part.get_filename()
                attachment['body'] = part.get_content()
                email_dict['attachments'].append(attachment)

        emails.append(email_dict)

    return emails


def zmq_master():
    ''' Main app logic, threads start from here.'''
    context = zmq.Context.instance()
    server = context.socket(zmq.REP)
    server.bind("inproc://zmq")  # "tcp://*:5555")
    thread = threading.Thread(target=zmq_slave)
    thread.daemon = True
    thread.start()

    while True:
        request = server.recv()
        request = msgpack.unpackb(request)
        payload = None

        if request[0] == 0:
            get_error = False
            requests_timeout = (5, 30)
            try:
                requests_get = requests.get(
                    URL,
                    timeout=requests_timeout)
                requests_get.raise_for_status()
            except requests.exceptions.HTTPError as requests_exception:
                get_error = True
                print('HTTP error: {}'.format(requests_exception))
            except requests.exceptions.RequestException as requests_exception:
                get_error = True
                print('Connection eror: {}'.format(requests_exception))

            if get_error:
                print('\n\tProviding UID locally\n')
                payload = 0
            else:
                payload = requests_get.json()[0]
        elif request[0] == 1:
            if request[1]:
                print('\n\tNew mails arrived.\n')
                new_emails = parse_email(request[1])
                post_error = False
                requests_timeout = (5, 30)
                try:
                    requests_post = requests.post(
                        URL,
                        timeout=requests_timeout,
                        data=json.dumps(new_emails, default=str))
                    requests_post.raise_for_status()
                except requests.exceptions.HTTPError as requests_exception:
                    post_error = True
                    print('HTTP error: {}'.format(requests_exception))
                except requests.exceptions.RequestException as\
                        requests_exception:
                    post_error = True
                    print('Connection eror: {}'.format(requests_exception))

                if post_error:
                    for new_email in new_emails:
                        print(
                            "\n\tI've got the email with the following subject:\
                             \n\n\t\t{}\n"
                            .format(new_email['metadata']["Subject"].upper()))

                        if new_email['attachments']:
                            print('\t\tAttachments:\n')

                            for attachment in new_email['attachments']:
                                print(
                                    '\t\t\t[Filename]: {:<30} [Size]: {:<10} \
                                            [MIME]: {:<8}\n'
                                    .format(attachment['filename'],
                                            len(attachment['body']),
                                            attachment['MIME']))

            else:
                print('\n\tNo new emails.\n')
        reply = msgpack.packb([request[0], payload])
        server.send(reply)

    server.close()
    context.term()


def fetch_emails(
        username,
        password,
        uid=0,
        address='imap.gmail.com',
        port=993,
        mail_batch_limit=5,    # Если писем много, то качаем пачкой.
        mail_total_limit=10):  # Временное ограничение на общее кол-во писем.
    ''' Returns up to "mail_batch_limit" new emails from INBOX per run
        touches no more than "mail_total_limit" mails per multiple runs'''

    imap_connect = IMAP4_SSL(address, port)              # Подключаемся.
    imap_connect.login(username, password)               # Логинимся.
    # Подключаемся к INBOX. Readonly, чтобы не сбросить статус "Не прочитано".
    imap_connect.select(mailbox='INBOX', readonly=True)
    # Если передан UID, то читаем всё, что новее. Иначе читаем все письма.
    imap_uid_string = 'UID {}:*'.format(int(uid) + 1) if uid else 'ALL'

    # Получаем tuple из бинарных статуса ответа и строки uid писем.
    reply_numbers, data_numbers = imap_connect.uid('search',
                                                   None,
                                                   imap_uid_string)

    if reply_numbers == 'OK':
        uid_bin = data_numbers[0].split()  # Получаем список бинарных чисел.
        len_uid_bin = len(uid_bin)
        more_mails = False
        last_uid = uid
        result = False

        if len_uid_bin <= 1:
            if uid_bin[0] > str(uid).encode():
                last_uid = uid_bin[0].decode()

            return last_uid, more_mails, result

        elif len_uid_bin > mail_batch_limit:
            more_mails = True

            if len_uid_bin > mail_total_limit:
                uid_bin = uid_bin[-mail_total_limit:]

            uid_bin = uid_bin[:mail_batch_limit]

        result = list()
        reply_email, data_email = imap_connect.uid('fetch',
                                                   b','.join(uid_bin),
                                                   '(RFC822)')

        if reply_email == 'OK':
            for i in range(0, len(data_email), 2):
                imap_info = data_email[i][0].split()
                # Это строка вида: b'id (UID xx RFC822 {byte_length} ('
                uid_email = imap_info[2]        # UID
                len_email = imap_info[4][1:-1]  # {byte_length}
                raw_email = data_email[i][1]
                result.append((uid_email, len_email, raw_email))

            last_uid = uid_email.decode()

            return last_uid, more_mails, result

        return '{} returned error: {}'.format(address, reply_email)

    else:
        return '{} returned error: {}'.format(address, reply_numbers)


def zmq_slave():
    ''' ZMQ '''

    request_timeout = 2500
    request_retries = 3
    server_endpoint = "inproc://zmq"  # "tcp://localhost:5555"

    # context = zmq.Context(1)
    context = zmq.Context.instance()

    # print("[Slave]  I've come to life! Connecting to server...")
    client = context.socket(zmq.REQ)
    client.connect(server_endpoint)

    poll = zmq.Poller()
    poll.register(client, zmq.POLLIN)

    # sequence = 0
    retries_left = request_retries
    expect_reply = False
    phase = 0
    more_mails = None
    last_uid = None
    more_new_mails_flag = False

    while True:
        if not expect_reply:
            payload = None

            if phase == 1:
                if not more_mails:
                    last_uid = last_uid or reply[1]
                    last_uid, more_new_mails_flag, mails = fetch_emails(
                        imap_username, imap_password, last_uid,
                        imap_server, imap_port, 5, 10)

                if mails:
                    payload = mails
            request = msgpack.packb([phase, payload])
            client.send(request)

            if phase == 1 and not more_mails and not more_new_mails_flag:
                time.sleep(10)

        expect_reply = True

        while expect_reply:
            socks = dict(poll.poll(request_timeout))

            if socks.get(client) == zmq.POLLIN:
                reply = client.recv()

                if not reply:
                    break
                reply = msgpack.unpackb(reply)
                retries_left = request_retries

                if phase < 1:
                    phase = reply[0] + 1
                expect_reply = False

            else:

                if retries_left > 0:
                    retries_left -= 1

                    break
                client.setsockopt(zmq.LINGER, 0)
                client.close()
                poll.unregister(client)
                client = context.socket(zmq.REQ)
                client.connect(server_endpoint)
                poll.register(client, zmq.POLLIN)
                retries_left = request_retries
                client.send(request)

    client.close()
    # context.term()


if __name__ == '__main__':
    zmq_master()
