from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)

    def send_customer_mail(self):
        subject = 'Заказ робота'
        model, version = self.robot_serial.split('-')
        message = 'Добрый день!\n' \
                  'Недавно вы интересовались нашим роботом модели {}, версии {}.\n' \
                  'Этот робот теперь в наличии. ' \
                  'Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'.format(model, version)

        send_mail(
            subject=subject,
            message=message,
            from_email='example@mail.com',
            recipient_list=[self.customer.email],
        )
