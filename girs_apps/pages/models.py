from django.db import models
from girs_apps.account.models import User

class LocationCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Location Name")
    description = models.TextField(verbose_name="Location Description")
    category = models.ForeignKey(LocationCategory, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="location_images", verbose_name="Location Image")

    def __str__(self):
        return self.name