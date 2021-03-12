from django.db import models
import datetime

class GeoPhoto(models.Model):
    title = models.CharField(max_length=250)
    latitude=models.FloatField()
    longitude=models.FloatField()
    photo_url = models.CharField(max_length=500, unique=True)
    date_added = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.title
    
class PresetList(models.Model):
    name = models.CharField(max_length=250)
    latitude=models.FloatField()
    longitude=models.FloatField()
    date_added = models.DateField(default=datetime.datetime.now)

    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return self.name

class FavList(models.Model):
    geophoto = models.ForeignKey(GeoPhoto, on_delete=models.CASCADE)
    date_added = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.geophoto.title
