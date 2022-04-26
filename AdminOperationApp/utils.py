from django.core.mail import EmailMessage
import asyncio


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
    def send_email_attach(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.attach_file(data['file_path'])
        email.send()

async def send_mail2(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    # await asyncio.sleep(1)

    email.send()
