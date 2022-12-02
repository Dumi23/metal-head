from .models import AlbumRated

def average_calc(idAlbum):
    try: 
        avg = float(AlbumRated.objects.get(idAlbum = idAlbum).Rating / AlbumRated.objects.filter(idAlbum = idAlbum).count())
        return avg
    except AlbumRated.DoesNotExist:
        return 0