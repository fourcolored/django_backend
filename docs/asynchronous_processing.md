# Message Queues and Asynchronous Processing
Message queues are used for asynchonous communication between components of the system. Aynchronous processing executes tasks in background without delaying user interactions.


I use Celery and RabbitMQ for asynchronous processing tasks on the background.

**Sending order confirmation emails:** sends emails on the background when order is created
```
@shared_task
def sending_order_confirmation_email(order_id, user_email):
    
    send_mail(
        subject=f"Order confirmation: {order_id}",
        message="Order is confirmed, wait for the further actions",
        recipient_list=[user_email],
        from_email='ecommerce@email.com',
    )
    
    logger.debug("[INFO] [Celery-sending_order_confirmation_email] Email confirmation")
```

**Output**

```
final-celery-1  | [2024-12-12 22:54:57,042: DEBUG/ForkPoolWorker-1] [INFO] [Celery-sending_order_confirmation_email] Email confirmation

final-celery-1  | [2024-12-12 22:54:57,042: INFO/ForkPoolWorker-1] Task store.tasks.sending_order_confirmation_email[4660a744-a5a8-4532-86f2-a113069d1c0b] succeeded in 0.0015127360020414926s: None
```


**Processing payment**: changes status of the payment and order after order is done
```
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
```
**Output**

```
final-celery-1  | [2024-12-12 22:54:57,051: DEBUG/ForkPoolWorker-16] [INFO] [Celery-payment_processing] Payment 1 successfull 

final-celery-1  | [2024-12-12 22:54:57,051: INFO/ForkPoolWorker-16] Task store.tasks.processing_payment[c55dc073-b9aa-4401-b9b2-a9481fcc67a9] succeeded in 0.010743724000349175s: None
```