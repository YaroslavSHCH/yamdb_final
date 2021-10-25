from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_confirm_code(email, confirmation_code):
    """
    Отправляет на email пользователя сообщение с кодом потверждения.
    """
    subject = 'Yambd: Проверочнный код'
    html_message = render_to_string(
        'confirmation_key_page.html', {'code': confirmation_code}
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    mail.send_mail(subject, plain_message, from_email, [to],
                   html_message=html_message)
