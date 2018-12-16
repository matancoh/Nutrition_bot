from smtplib import SMTP
recipients = ['matan.cohen@gmail.com'] #, 'zimerman@gmail.com', 'meidan89@gmail.com']


with open('UserKeepLocal.txt','r') as f:
    user = f.readline()[:-1]
    password = f.readline()


def send_email (message, status):
    fromaddr = 'MTA.SADNA2018@gmail.com'
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user , password)
    server.sendmail(fromaddr, recipients, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

 send_email("menu content","Menu from Nutrition Bot")