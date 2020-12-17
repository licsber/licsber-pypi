import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from licsber.utils import get_now_date


def _parse_dict(detail: dict) -> str:
    res = ''
    for i in detail:
        res += str(i) + ': ' + str(detail[i]) + '<br>'
    return res


class SMTP:
    def __init__(self, password,
                 mail_address='silverwings233@qq.com',
                 smtp_server='smtp.qq.com',
                 sender=None,
                 username=None):
        if not sender:
            sender = mail_address
        if not username:
            username = mail_address
        self.sender = sender
        self.smtp = smtplib.SMTP()

        self.smtp.connect(smtp_server)
        self.smtp.login(username, password)

    def plain_mail_to(self, title: str, body: str,
                      receiver=None,
                      mail_from='Licsber Automatic'):
        if not receiver:
            receiver = self.sender
        msg = MIMEText(body, 'plain', 'utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['From'] = mail_from
        msg['To'] = receiver
        msg['Subject'] = Header(title, 'utf-8')

        try:
            self.smtp.sendmail(self.sender, receiver, msg.as_string())
            return True
        except smtplib.SMTPException:
            return False

    def notice_mail_to(self, mail_title: str, title: str, detail: any,
                       receiver=None,
                       mail_from='Licsber Automatic'):
        if not receiver:
            receiver = self.sender

        if type(detail) is dict:
            detail = _parse_dict(detail)

        mail_title = get_now_date() + ' ' + mail_title

        msg = MIMEMultipart('alternative')

        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['From'] = mail_from
        msg['To'] = receiver
        msg['Subject'] = Header(mail_title, 'utf-8')
        template_path = os.path.join(os.path.dirname(__file__), 'notice_template.html')
        html = open(template_path).read()
        html = html.replace('{{title}}', title)
        html = html.replace('{{detail}}', detail)

        html = MIMEText(html, 'html')
        msg.attach(html)

        try:
            self.smtp.sendmail(self.sender, receiver, msg.as_string())
            return True
        except smtplib.SMTPException:
            return False
