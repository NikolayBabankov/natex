import smtplib as smtp
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def sendEmail(dictLead):
    email = settings.LOGIN_EMAIL
    password = settings.PASS_EMAIL
    dest_email = settings.DEST_EMAIL
    subject = f'{settings.SUB_EMAIL} - {dictLead["date"]}'
    email_text = f'Имя: {dictLead["name"]}\n\n Телефон: {dictLead["phone"]} \n\n Дата: {dictLead["date"]}'
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest_email,
                                                           subject,
                                                           email_text)
    try:
        server = smtp.SMTP_SSL(settings.SMTP_EMAIL)
        server.ehlo(email)
        server.login(email, password)
        server.auth_plain()
        server.sendmail(email, dest_email,
                        message.format(dest_email, message).encode('utf-8'))
        server.quit()
    except:
        logger.warning(dictLead)
        return False

    return True
