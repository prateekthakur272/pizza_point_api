from settings import get_settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP_SSL
from jinja2 import Environment, FileSystemLoader
from models import User


settings = get_settings()

def _render_temlate(path:str, data:dict)->str:
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template(path)
    return template.render(data)

async def send_mail(message:MIMEBase):
    with SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_SERVER_PORT) as smtp:
        smtp.login(settings.EMAIL, settings.PASSWORD)
        smtp.send_message(message)
        
async def send_verification_mail(user:User, token:str):

    template = _render_temlate('verify_account.html', {'token':token, 'username':user.username})
    
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Pizza-Point Account Verification'
    message['To'] = user.email
    message['From'] = settings.EMAIL
    
    html = MIMEText(template, 'html')
    text = MIMEText('email not supported', 'plain')
    
    message.attach(text)
    message.attach(html)
    
    await send_mail(message)