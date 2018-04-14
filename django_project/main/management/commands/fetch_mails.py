from django.core.management.base import BaseCommand, CommandError
from main.models import Mail, Mail_Account
# from imap import fetch_emails 
from datetime import datetime
from email.parser import BytesParser
from email.policy import default
from imaplib import IMAP4_SSL

class Command(BaseCommand):
    help = 'get mails'
    

    def fetch_emails(self, addr, port, user, pwd,
                     uid=None, mail_limit=10, commit_limit=5):
        ''' returns up to "commit_limit" new emails from INBOX per run
            touches no more than "mail_limit" mails per multiple runs'''

        def fetch_and_parse(uids):
            ''' fetches and parses up to "commit_limit" new emails '''

            result = list()

            for uid in uids:
                email_dict = dict()
                reply, email_data = imap_server.uid('fetch', uid, '(RFC822)')
                if reply == 'OK':
                    raw_email = email_data[0][1]
                    email = BytesParser(policy=default).parsebytes(raw_email)
                    email_dict['Date'] = datetime.strptime(
                        email['Date'], '%a, %d %b %Y %H:%M:%S %z')

                    for header in ['From', 'To', 'Delivered-To',
                                   'Message-ID', 'Subject']:
                        email_dict[header] = email[header]
                    email_dict['plain'] = None
                    email_dict['html'] = None
                    for part in email.walk():
                        if part.get_content_type() == 'text/html':
                            email_dict['html'] = part.get_body().get_content()
                        elif part.get_content_type() == 'text/plain':
                            email_dict['plain'] = part.get_body().get_content()
                    result.append(email_dict)

            return result

        imap_server = IMAP4_SSL(addr)
        imap_server.login(user, pwd)
        imap_server.select(mailbox='INBOX', readonly=True)

        if uid:
            reply, data = imap_server.uid('search', None, '{}:*'.format(uid))
        else:
            reply, data = imap_server.uid('search', None, 'ALL')
            uid = 0

        if reply == 'OK':
            uids_blist = data[0].split()
            len_uids_blist = len(uids_blist)

            if len_uids_blist < 2:
                if uids_blist[0] > str(uid).encode():
                    #fetch_and_parse(uids_blist)

                    # return '1 new mail'
                    return int(uids_blist[0].decode()), False, fetch_and_parse(uids_blist)

                # return '0 new mails'
                return uid, False, False
            elif len_uids_blist > commit_limit:
                if len_uids_blist > mail_limit:
                    #fetch_and_parse(uids_blist[-mail_limit:][:commit_limit])
                            return int(uids_blist[-mail_limit:][:commit_limit][-1].decode()), True, fetch_and_parse(uids_blist[-mail_limit:][:commit_limit])
                #else:
                    #fetch_and_parse(uids_blist[:commit_limit])
                return int(uids_blist[:commit_limit][-1].decode()), True, fetch_and_parse(uids_blist[:commit_limit])

                # return 'Many new mails'
            else:
                #fetch_and_parse(uids_blist)

                #return 'Some new mails'
                return int(uids_blist[-1].decode()), False, fetch_and_parse(uids_blist)
        else:
            return 'Something wrong'

    def handle(self, *args, **options):
            for account in Mail_Account.objects.all():
                new_mails = 'Possibly :-)'
                new_uid = account.last_uid
                while new_mails:
                    new_uid, new_mails, mail_list = self.fetch_emails(account.server, account.port, account.email, account.password, new_uid)
                    if mail_list:
                        for i in mail_list:
                            mail = Mail(
                                _delivered_to=account, _to=i['To'], _from=i['From'], _subject=i['Subject'], 
                                _date=i['Date'], _message_id=i['Message-ID'], text=i['plain'] or '', html=i['html'] or '')
                            mail.save()
                        account.last_uid = new_uid
                account.save()
    '''
    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
            '''