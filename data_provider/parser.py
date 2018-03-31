#!/usr/bin/env python
''' docstring '''
from random import randint
import time
import zmq
import json
from datetime import datetime
from email.policy import default
from email.parser import BytesParser


def parse_email(raw_email_decoded):
    ''' parse email '''

    email_dict = dict()
    raw_email = raw_email_decoded.encode()
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

    return email_dict

def zmq_master():
    context = zmq.Context(1)
    server = context.socket(zmq.REP)
    server.bind("tcp://*:5555")
    print("[Master] I'm alive! Waiting for slaves to ask for my orders...")

    payload = None
    while True:
        request = server.recv_json()
        e = json.loads(request)
        print(e[3])
        time.sleep(1) # Do some heavy work
        if e[2] == 0:
            words = "[Master] Then serve me! What can you do?"
        elif e[2] == 1:
            words = "[Master] Then get me some emails!"
        elif e[2] == 2:
            payload = 0
            words = "[Master] The last UID you checked was {}.".format(payload)
        elif e[2] == 3:
            if e[4]:
                new_email = parse_email(e[4][2])
                print("\n\tI've got the email with the following subject:\n\n\t\t{}\n".format(new_email['metadata']["Subject"].upper()))
                if new_email['attachments']:
                    print('\tAttachments:\n')
                    for h in new_email['attachments']:
                        print('\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'.format(h['filename'], len(h['body']), h['MIME']))
                words = "[Master] Good boy, get me more."
            else:
                words = "[Master] Then check again!"
        else:
            words = "[Master] What are you mumbling?!"
        r = json.dumps([e[0], "Master", e[2], words, payload])
        server.send_json(r)
        print(words)

    server.close()
    context.term()


if __name__ == '__main__':
    zmq_master()
