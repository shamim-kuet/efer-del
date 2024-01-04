import random
import string
import threading
from django.core.mail import EmailMessage
from django.conf.global_settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_referral_code_generator(instance, name):
    uuid_new_id = random_string_generator(size=6)
    # Klass = instance.__class__
    qs_exists = instance.objects.filter(referral_code=uuid_new_id).exists()
    if qs_exists:
        return random_string_generator(instance)
    if name:
        return f'{name.split()[0]}_' + uuid_new_id
    return f'{name}_' + uuid_new_id


def unique_uuid_generator(instance):
    uuid_new_id = random_string_generator(size=6, chars=string.digits)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(uuid=uuid_new_id).exists()
    if qs_exists:
        return unique_uuid_generator(instance)
    return uuid_new_id