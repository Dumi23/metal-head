from .models import AlbumRated
from django.db.models import Avg

def average_calc(idAlbum):
        avg = AlbumRated.objects.filter(idAlbum=idAlbum).aggregate(Avg('Rating'))
        print(avg.values())
        if avg['Rating__avg'] == None:
            return 0 
        return avg['Rating__avg']
