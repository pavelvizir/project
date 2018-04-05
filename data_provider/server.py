#!/usr/bin/env python
'''
'''

import json
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST'])
def show_emails():
    if request.method == 'GET':
        return json.dumps([0, ])
    else:
        new_emails = request.get_json(force=True)
        for new_email in new_emails:
            print("\n\tI've got the email with the following subject:\n\n\t\t{}\n".format(new_email['metadata']["Subject"].upper()))
            if new_email['attachments']:
                print('\t\tAttachments:\n')
                for h in new_email['attachments']:
                    print('\t\t\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'.format(h['filename'], len(h['body']), h['MIME']))
        resp = make_response('preved', 200)
        resp.headers['X-Something'] = 'A value'
        return resp


if __name__ == '__main__':
    app.run()
