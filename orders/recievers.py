from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def send_message(sender, instance, **kwargs):
    last_created_robot = Robot.objects.last()
    orders = Order.objects.filter(robot_serial=last_created_robot.serial).all()
    for order in orders:
        order.send_customer_mail()
