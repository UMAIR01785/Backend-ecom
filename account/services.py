from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings




def send_verfication_mail(user,activate_link):
    subject="Activate the account"
    from_email=settings.EMAIL_HOST_USER
    to=[user.email]

    context={
        'user':user,
        'activate_link':activate_link
    }
    text_body = render_to_string("activate_account.txt", context)
    html_body = render_to_string("activate_account.html", context)

    email=EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to
    )
    email.attach_alternative(html_body,'text/html')
    email.send()
    


def reset_email(user,activate_link):
    subject="Reset the password"
    from_email=settings.EMAIL_HOST_USER
    to=[user.email]

    context={
        'user':user,
        'activate_link':activate_link
    }

    text_body=render_to_string('reset.txt' ,context)
    html_body=render_to_string('reset.html',context)


    email=EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to
    )

    email.attach_alternative(html_body ,'text/html')
    email.send()