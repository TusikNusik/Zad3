from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("points", views.points, name="points"),
    path("addList", views.addList, name="addList"),
    path("addPoint/<int:id>", views.addPoint, name="addPoint"),
    path("savedProjects", views.savedProjects, name="savedProjects")
]