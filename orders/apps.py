from django.apps import AppConfig
from django.db.models.signals import post_save


class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        from orders.recievers import send_message
        from robots.models import Robot
        from orders.models import Order
        post_save.connect(send_message, sender=Robot)
