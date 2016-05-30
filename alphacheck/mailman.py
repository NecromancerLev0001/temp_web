import smtplib
from email.mime.text import MIMEText

FROMADDR = 'mm7vo0@gmail.com'
TOADDRS  = 'kanobaoha@gmail.com'
USERNAME = 'mm7vo0@gmail.com'
PASSWORD = '88*uudK%72'

def snd_ml(subject_txt, body_txt):
    # make msg
    msg = MIMEText(body_txt)  
    msg['Subject'] = subject_txt
    msg['From'] = FROMADDR
    msg['To'] = TOADDRS
    # Login
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(USERNAME, PASSWORD)
    # Sending the mail  
    server.sendmail(FROMADDR, TOADDRS, msg.as_string())
    server.quit()

if __name__ == '__main__':
    #pass
    snd_ml('dey~', 'dey~ dey~ dey~ dey~ dey~')
