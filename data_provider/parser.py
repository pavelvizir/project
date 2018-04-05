#!/usr/bin/env python
''' docstring '''
# from random import randint
# import time
import zmq
import json
import msgpack
from datetime import datetime
from email.policy import default
from email.parser import BytesParser
import requests

URL = 'http://127.0.0.1:5000/api'

def parse_email(raw_emails):
    ''' parse email '''
    emails = list()
    for uid, length, raw_email in raw_emails:
        email_dict = dict()
        email = BytesParser(policy=default).parsebytes(raw_email)
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
    context = zmq.Context(1)
    server = context.socket(zmq.REP)
    server.bind("tcp://*:5555")

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
                except requests.exceptions.RequestException as requests_exception:
                    post_error = True
                    print('Connection eror: {}'.format(requests_exception))
                if post_error:
                    for new_email in new_emails:
                        print("\n\tI've got the email with the following subject:\n\n\t\t{}\n".format(new_email['metadata']["Subject"].upper()))
                        if new_email['attachments']:
                            print('\t\tAttachments:\n')
                            for h in new_email['attachments']:
                                print('\t\t\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'.format(h['filename'], len(h['body']), h['MIME']))
 
            else:
                print('\n\tNo new emails.\n')
        reply = msgpack.packb([request[0], payload])
        server.send(reply)

    server.close()
    context.term()


if __name__ == '__main__':
    zmq_master()
