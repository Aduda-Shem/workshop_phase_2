from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_activation_email(request, user, password):
    activation_link = request.build_absolute_uri(reverse('activate_account', args=[user.activation_code]))
    subject = 'Activate your account'
    message = f'Please click the following link to activate your account: {activation_link}\n\n'
    message += f'Your generated password is: {password}\n\n'
    message += 'Please keep this information secure.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def send_registration_email(request, user, password):
    subject = 'Employee Registration Confirmation'
    message = f'Welcome OnBoard. You have been registered as an employee.\n\n'
    message += f'Your account has been created. You can now log in using the following credentials:\n\n'
    message += f'Email: {user.email}\n'
    message += f'Password: {password}\n\n'
    message += 'Please keep this information secure.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)