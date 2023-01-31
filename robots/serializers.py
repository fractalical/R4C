from rest_framework import serializers

from robots.models import Robot


class RobotWriteSerializer(serializers.Serializer):
    serial = serializers.CharField(max_length=5)
    model = serializers.CharField(max_length=2)
    version = serializers.CharField(max_length=2)
    created = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    def validate_model(self, value):
        available_models = ['R2', 'C3', 'X5', '13', 'R6', 'R7']  # data may be load from db
        if value.upper() not in available_models:
            raise serializers.ValidationError("This model is not exist!")
        return value

    def create(self, validated_data):
        return Robot.objects.create(**validated_data)
