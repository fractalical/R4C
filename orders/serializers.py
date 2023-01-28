from rest_framework import serializers


class OrderCreateSerializer(serializers.Serializer):
    customer = serializers.EmailField()
    robot_serial = serializers.CharField(max_length=5)
