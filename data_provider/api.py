#!/usr/bin/env python
''' Test API for parser. '''

import json
from flask import Flask, request, make_response

APP = Flask(__name__)


@APP.route('/api', methods=['GET', 'POST'])
def api():
    ''' Returns 0 for GET, receives and displays emails for POST.'''

    if request.method == 'GET':
        return json.dumps([0, ])

    # Достаём темы и сложения, чтобы продемонстрировать пришедший json.
    new_emails = request.get_json(force=True)
    for new_email in new_emails:
        print("\n\tI've got the email with the following subject:\n\n\t\t{}\n"
              .format(new_email['metadata']["Subject"].upper()))
        if new_email['attachments']:
            print('\t\tAttachments:\n')
            for attachment in new_email['attachments']:
                print('\t\t\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'
                      .format(attachment['filename'],
                              len(attachment['body']),
                              attachment['MIME']))

    # Flask требует возвращать response на POST в правильном формате.
    resp = make_response('preved', 200)
    resp.headers['X-Something'] = 'A value'
    return resp


if __name__ == '__main__':
    APP.run()
