from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from orders.models import Order
from orders.serializers import OrderCreateSerializer
from orders.tasks import send_notification
from robots.models import Robot


class OrderCreationView(APIView):
    order_serializer = OrderCreateSerializer
    def post(self, request):
        order_data = request.data
        data_to_write = self.order_serializer(data=order_data)
        valid = data_to_write.is_valid(raise_exception=True)
        customer_to_write = Customer(email=order_data['customer'])
        order_to_write = Order(customer=customer_to_write, robot_serial=order_data['robot_serial'])
        customer_to_write.save()
        order_to_write.save()

        order_id = order_to_write.id
        if order_data['robot_serial'] not in Robot.objects.values_list('serial', flat=True).distinct():
            send_notification.delay(order_id)

        return Response(data=order_data, status=status.HTTP_201_CREATED)
