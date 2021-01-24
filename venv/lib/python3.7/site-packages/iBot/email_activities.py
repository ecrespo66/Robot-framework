import smtplib
from imap_tools import MailBox, Q
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import os


class Mail:

    def __init__(self, email, password):
        self.username = email
        self.password = password

    def send(self, send_to, subject, text=None, html=None, files=None):

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(send_to)
        msg['Subject'] = subject

        if text is not None:
            msg.attach(MIMEText(text + "\n\n\n", 'plain'))

        if html is not None:
            msg.attach(MIMEText(html + "\n\n\n", 'html'))

        for f in files or []:
            with open(f, "rb") as fil:
                ext = f.split('.')[-1:]
                attachedfile = MIMEApplication(fil.read(), _subtype=ext)
                attachedfile.add_header(
                    'content-disposition', 'attachment', filename=basename(f))
            msg.attach(attachedfile)

        smtp = smtplib.SMTP_SSL('smtp.' + self.username.split("@")[1], 465)
        smtp.ehlo()

        smtp.login(self.username, self.password)

        smtp.sendmail(self.username, send_to, msg.as_string())

        smtp.close()

    def fetchBox(self, folder=None, Query=None):

        if folder is None:
            folder = 'INBOX'

        if Query is None:
            Query = Q(all=True)

        server = 'imap.' + self.username.split("@")[1]
        mailbox = MailBox(server)
        mailbox.login(self.username, self.password, initial_folder=folder)  # or mailbox.folder.set instead 3d arg

        message_list = []
        for mail in mailbox.fetch(Query):
            message_list.append(mail)

        return message_list

        mailbox.logout()

    @staticmethod
    def save_attachments(email, download_folder):

        msg = email.obj

        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path


'''import win32com
import win32com.client
    
def folders():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace('MAPI')
    
    Folders={}
    fList = [3,4,5,6,23]
    for i in fList:
        try:
            folder = outlook.GetDefaultFolder(i)
            Folders[folder.name] = i
        except:
            pass
    
    return(Folders)

def accounts():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace('MAPI')
    for account in outlook.Folders:
        return account.name
    

class outlook:

    def __init__ (self):
        
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.folders = folders()
        self.accounts = accounts()
        
    def emails(self,folder):
        
        i= folders()[folder]
        Folder= self.outlook.GetDefaultFolder(i)
        messages = Folder.Items
        
        MessageList=[]
        
        for message in messages:
            MessageList.append(message)
        
        return MessageList
    
    
    def DownloadAttachments(self, email, folder, extension = None):    
        
        Attachments= email.Attachments
        AttachmentNum = Attachments.Count
        
        
        if AttachmentNum > 0:
                
            try:
                for i in range(1,int(AttachmentNum)):
                    
                    fileType = str(Attachments.item(i)).split(".")[1]
                    fileType = fileType.lower()
                    
                    if extension == None:
                        if fileType != "png" and fileType != "jpg" and  fileType != "jpeg" and  fileType != "gif":

                            Attachments.Item(i).SaveASFile(folder + str(Attachments.item(i)))
                    else:
                        
                        if fileType == extension.replace(".",""):
                            
                            Attachments.Item(i).SaveASFile(folder + str(Attachments.item(i))) 
            except:
                pass
            
    
    def SendEmail(self,To,Subject,Body, Attachment= None):
        
        
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = To
        mail.Subject = Subject
        mail.Body = Body
        #mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional
        
        if Attachment != None:
            attachment  = Attachment 
            mail.Attachments.Add(attachment)

        mail.Send()
    
'''
