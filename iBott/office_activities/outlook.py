
class Outlook:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.folders = self.folders()
        self.accounts = self.accounts()

    def emails(self, folder):

        i = self.folders()[folder]
        Folder = self.outlook.GetDefaultFolder(i)
        messages = Folder.Items

        MessageList = []

        for message in messages:
            MessageList.append(message)

        return MessageList

    def DownloadAttachments(self, email, folder, extension=None):

        Attachments = email.Attachments
        AttachmentNum = Attachments.Count

        if AttachmentNum > 0:

            try:
                for i in range(1, int(AttachmentNum)):

                    fileType = str(Attachments.item(i)).split(".")[1]
                    fileType = fileType.lower()

                    if extension == None:
                        if fileType != "png" and fileType != "jpg" and fileType != "jpeg" and fileType != "gif":
                            Attachments.Item(i).SaveASFile(folder + str(Attachments.item(i)))
                    else:

                        if fileType == extension.replace(".", ""):
                            Attachments.Item(i).SaveASFile(folder + str(Attachments.item(i)))
            except:
                pass

    @staticmethod
    def SendEmail(To, Subject, Body, Attachments=None):

        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        if isinstance(To, list):
             To = "; ".join(To)
        mail.To = To
        mail.Subject = Subject
        mail.Body = Body
        # mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

        if Attachments is not None:
            for attachment in Attachments:
                mail.Attachments.Add(attachment)
        mail.Send()
    @staticmethod
    def folders():
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace('MAPI')

        Folders = {}
        fList = [3, 4, 5, 6, 23]
        for i in fList:
            try:
                folder = outlook.GetDefaultFolder(i)
                Folders[folder.name] = i
            except:
                pass

        return (Folders)

    @staticmethod
    def accounts():
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace('MAPI')
        for account in outlook.Folders:
            return account.name