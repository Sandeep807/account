from django.conf import settings
from django.core.mail import send_mail

def send_activate_email(email,first_name,activation_url):
    try:
        subject="Your account needs to verified"
        message=f'Hi{first_name} your otp to activate account is-{activation_url}'
        email_from=settings.EMAIL_HOST
        send_mail(subject,message,email_from,[email])
    except Exception as e:
        print(e)