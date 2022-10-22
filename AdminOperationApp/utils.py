from django.core.mail import EmailMessage,EmailMultiAlternatives
import asyncio


class Util:
    @staticmethod
    #=========================For sending normal email=================================
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
        
    #=========================For sending rendered email=================================
    def send_email_body(data):
        email = EmailMultiAlternatives(
            subject=data['email_subject'], to=[data['to_email']])
        email.attach_alternative(data['email_body'], "text/html")
        email.send()
        
    #=========================For sending email with attachment=================================
    def send_email_attach(data):
        email = EmailMultiAlternatives(
            subject=data['email_subject'], body=data['email_body'],to=[data['to_email']])
        email.attach_file(data['file_path'])
        email.send()
        
    #=========================For sending email with attachment and rendered body=================================
    def send_email_attach_body(data):
        email = EmailMultiAlternatives(
            subject=data['email_subject'], to=[data['to_email']],cc=['hr@techforing.com'])
        email.attach_file(data['file_path'])
        email.attach_alternative(data['email_body'], "text/html")
        email.send()

async def send_mail2(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    # await asyncio.sleep(1)

    email.send()
