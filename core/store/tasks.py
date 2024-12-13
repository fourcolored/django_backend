from celery import shared_task
from store.models import Order, Payment
from django.core.mail import send_mail
import logging
import time
logger = logging.getLogger('django')

@shared_task
def sending_order_confirmation_email(order_id, user_email):
    
    send_mail(
        subject=f"Order confirmation: {order_id}",
        message="Order is confirmed, wait for the further actions",
        recipient_list=[user_email],
        from_email='ecommerce@email.com',
    )
    
    logger.debug("[INFO] [Celery-sending_order_confirmation_email] Email confirmation")

@shared_task
def processing_payment(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        if payment.status == "PENDING":
            payment.status = "SUCCESS"
            payment.order.order_status = "COMPLETED"
            payment.save()
            payment.order.save()
            logger.debug(f"[INFO] [Celery-payment_processing] Payment {payment_id} successfull")
        else:
            logger.debug(f"[INFO] [Celery-payment_processing] Payment {payment_id} successfull")
    except Payment.DoesNotExist:
        logger.debug(f"[INFO] [Celery-payment_processing] Payment {payment_id} doesn't exist")