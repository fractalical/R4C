from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from robots.models import Robot
from robots.serializers import RobotWriteSerializer


def index_view(request):
    return HttpResponse('Hello there!')


class PostRobotsView(APIView):
    model = Robot
    serializer = RobotWriteSerializer

    def post(self, request):
        robot_data = request.data
        many = True if isinstance(robot_data, list) else False
        if isinstance(robot_data, list):
            many = True
            for i in range(len(robot_data)):
                try:
                    robot_data[i] = {"serial": f'{robot_data[i]["model"]}-{robot_data[i]["version"]}', **robot_data[i]}
                except KeyError as er:
                    return Response(er)
        elif isinstance(robot_data, dict):
            try:
                robot_data = {"serial": f'{robot_data["model"]}-{robot_data["version"]}', **robot_data}
            except KeyError as er:
                return Response(f'KeyError {str(er)}')
        else:
            return Response(data='TypeError', status=status.HTTP_400_BAD_REQUEST)
        data_to_write = self.serializer(data=robot_data, many=many)
        data_to_write.is_valid(raise_exception=True)
        data_to_write.save()

        return Response(data=data_to_write.data, status=status.HTTP_201_CREATED)
