from django.db.models import Max
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from mainapp.serializers import DataSerializer
from mainapp.models import Data

@csrf_exempt
@api_view(['POST'])
def create(request):
    data = JSONParser().parse(request)
    serializer = DataSerializer(data=data)  #конструктор с именоваными параметр
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def get_last_id(request):
    last_id = Data.objects.all().aggregate(Max('id'))
    return JsonResponse(last_id, status=status.HTTP_200_OK)
