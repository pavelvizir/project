from rest_framework import serializers
#AltEnter чтоб установить
from main.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data #model типа data, укащано какой класс мы сериализуем
        fields = ('id',
                  'PID',
                  'CID',
                  'Psource',
                  'Type',
                  'Metadata',
                  'Data_main',
                  'Additional_data',
                  'Link')
