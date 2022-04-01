from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()





"""
        ======== formatted email send =========
        html_message = render_to_string('html.html', context={})
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            'subject',
            plain_message,
            'pranto.techforing@gmail.com',
            ['zulkar.techforing@gmail.com']
        )
        email.attach_alternative(html_message,'text/html')
        email.send()
        email_body = plain_message
"""
