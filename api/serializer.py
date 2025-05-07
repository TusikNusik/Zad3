from rest_framework import serializers
from trasy.models import PointList, Point

class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointList
        fields = '__all__'

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'