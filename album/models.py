from django.db import models

# Create your models here.
class AlbumRated(models.Model):
    idAlbum = models.CharField(max_length=255, unique=True)
    Name = models.CharField(max_length=255)
    Artist = models.CharField(max_length=255) 
    Image = models.CharField(max_length=255)
    TotalTracks = models.IntegerField()
    Rating = models.IntegerField(default=0)
