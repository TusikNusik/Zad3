from django.contrib import admin

from .models import Point
from .models import PointList
from .models import BackgroundImage

admin.site.register(Point)
admin.site.register(PointList)
admin.site.register(BackgroundImage)