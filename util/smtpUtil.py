from data.dataVault import DataVault
from config import smtpConfig
import smtplib
from email.mime.text import MIMEText

class SMTPUtil:
    def sendEmailSSL(self, ptext, subject, recipient):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(smtpConfig.noreply, smtpConfig.passw)
        msg = MIMEText(ptext)
        msg['Subject'] = subject
        msg['From'] = smtpConfig.noreply
        msg['To'] = recipient
        server.sendmail(smtpConfig.noreply, [recipient], msg.as_string())
        server.quit()