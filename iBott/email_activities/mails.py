import smtplib
import ssl
from imap_tools import MailBox, Q, MailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import os


class Mail:
    """
    Mail class
    Arguments:
        email: str
        password: str
        smtp_server: str
        smtp_port: int
        imap_server: str
        imap_port: int
    Attributes:
        username: username of the mail account
        password: password of the mail account
        smtp_server: smtp server of the mail account
        smtp_port: smtp port of the mail account
        imap_server: imap server of the mail account
        imap_port: imap port of the mail account
    Methods:
          send(send_to, subject, text=None, html=None, files=None): send mail
          fetch(folder, Query) : fetch mail list from mail box use Query object and return MailMessage list
          find more information about Mail and Query objects here: https://pypi.org/project/imap-tools/0.16.1/#id2
    """

    Query = Q

    def __init__(self, email, password, smtp_server, smtp_port, imap_server, imap_port):
        self.username = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port
        setattr(MailMessage, 'download_attachments', self.download_attachments)

    def send(self, send_to, subject, text=None, html=None, files=None):
        """
        Send mail to email acount
            Arguments:
                send_to: email address to send to
                subject: subject of the email
                text: text of the email
                html: html of the email
                files: list of files to attach to the email
        """
        msg = MIMEMultipart()
        msg['From'] = self.username
        if isinstance(send_to, list):
            msg['To'] = ', '.join(send_to)
        else:
            raise ValueError("send_to must be a list")
        msg['Subject'] = subject

        if text is not None:
            msg.attach(MIMEText(text + "\n\n\n", 'plain'))

        if html is not None:
            msg.attach(MIMEText(html + "\n\n\n", 'html'))

        for f in files or []:
            with open(f, "rb") as fil:
                ext = f.split('.')[-1:]
                attached = MIMEApplication(fil.read(), _subtype=ext)
                attached.add_header(
                    'content-disposition', 'attachment', filename=basename(f))
            msg.attach(attached)

        context = ssl.create_default_context()
        smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.username, send_to, msg.as_string())
        smtp.close()

    def fetch(self, folder=None, Query=None):
        """
        Get list of emails from Mailbox server
        Arguments:
            folder: Folder to fetch emails from
            Query: Query to filter emails
        Returns:
            List of MailMessage objects
        """
        if folder is None:
            folder = 'INBOX'
        if Query is None:
            Query = Q(all=True)
        mailbox = MailBox(self.imap_server, self.imap_port)
        mailbox.login(self.username, self.password, initial_folder=folder)

        message_list = []
        for mail in mailbox.fetch(Query):
            message_list.append(mail)
        mailbox.logout()
        return message_list

    @staticmethod
    def download_attachments(mail, download_folder, extension=None):
        """
        Download Mail attachments
        Arguments:
            mail: MailMessage object
            download_folder: folder to download attachments to
            extension: extension of the attachments to download
        """

        msg = mail.obj
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if extension:
                if extension in filename:
                    att_path = os.path.join(download_folder, filename)
                    if not os.path.isfile(att_path):
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
            else:
                att_path = os.path.join(download_folder, filename)
                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
        return att_path
