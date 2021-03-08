from iBot.email_activities import Mail

username= "ecrespo@ibott.io"
password ="Mariquinah3"
smpt_server = 'mail.ibott.io'
smtp_port= 465
imap_server = 'mail.ibott.io'
imap_port= 993


server = "mail.ibott.io"
send_to = ["oname.dohe@gmail.com"]
subject = "colita azul"
text= "Hola, \n soy un mail de prueba"

mail = Mail(username, password, smtp_server=smpt_server, smtp_port=smtp_port, imap_server=imap_server, imap_port=imap_port)
mail.send(send_to, subject=subject, text=text)


for mail in mail.fetchBox():
    print(mail.subject)