from rest_framework import serializers
from .models import AlbumRated

class AlbumRatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumRated
        exclude = ('id', )