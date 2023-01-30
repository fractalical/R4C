from celery import shared_task

from orders.models import Order
from robots.models import Robot


@shared_task(bind=True)
def send_notification(self, order_id):
    order = Order.objects.get(id=order_id)
    available_models = Robot.objects.values_list('model', flat=True).distinct()
    order_model, order_version = order.robot_serial.split('-')
    try:
        if order_model in available_models:
            available_versions = Robot.objects.filter(model=order_model).values_list('version', flat=True).distinct()
            if order_version in available_versions:
                order.send_customer_mail()
            else:
                raise Exception()
        else:
            raise Exception()
    except Exception as e:
        raise self.retry(exc=e, countdowm=30)
