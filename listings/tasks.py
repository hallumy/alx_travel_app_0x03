from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(email, booking_reference):
    send_mail(
        'Payment Confirmation',
        f'Your payment for booking {booking_reference} was successful.',
        'noreply@yourdomain.com',
        [email],
        fail_silently=False,
    )

def send_booking_confirmation_email(user_email, booking_id):
    subject = 'Booking Confirmation'
    message = f'Thank you for your booking! Your booking ID is {booking_id}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)
    return f"Email sent to {user_email} for booking {booking_id}"
