from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BackgroundImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='background/')

    def __str__(self):
        return self.name

class Point(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    included = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.x},{self.y})"

class PointList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    backgroundImage = models.ForeignKey(BackgroundImage, on_delete=models.CASCADE, default=3)
    points = models.ManyToManyField(Point, related_name='point_lists')

    def __str__(self):
        return f"{self.name}"

    