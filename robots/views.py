import datetime
import os

import xlwt
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from robots.models import Robot
from robots.serializers import RobotWriteSerializer


def index_view(request):
    return HttpResponse('Hello there!')


class GetRobotsCountView(APIView):

    def get(self, request):
        models = Robot.objects.values_list('model', flat=True).distinct()
        book = xlwt.Workbook(encoding='utf-8')
        date = datetime.datetime.today() - datetime.timedelta(weeks=2)

        for model in models:
            if Robot.objects.filter(model=model, created__gt=date).count() > 0:
                sheet1 = book.add_sheet(f'model_{model}')
                sheet1.write(0, 0, 'Модель')
                sheet1.write(0, 1, 'Версия')
                sheet1.write(0, 2, 'Количество за неделю')
                versions = Robot.objects.filter(model=model,
                                                created__gt=date).values_list('version', flat=True).distinct()
                i = 1
                for version in versions:
                    count = Robot.objects.filter(model=model, version=version, created__gt=date).count()
                    if count > 0:
                        sheet1.write(i, 0, model)
                        sheet1.write(i, 1, version)
                        sheet1.write(i, 2, count)
                        i += 1
        excel_name = os.getcwd() + '\\robots_count.xls'
        book.save(excel_name)

        file_path = excel_name
        FilePointer = open(file_path, mode="rb")
        response = HttpResponse(FilePointer, content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename=robots_count.xls'

        return response