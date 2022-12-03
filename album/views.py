from django.db.models import Avg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .helper import average_calc
from .serializers import AlbumRatedSerializer
# Create your views here.
from spotipy.oauth2 import SpotifyClientCredentials
from .models import AlbumRated
import spotipy
import json

ClientID = "a0f03799e3bd4048bfbbcfc4e0850b6d"
ClientSecret = "27ff31beecaa44628a7f43dd1ab91335"

class GetAlbum(APIView):
    def get(self, request, q):    
        auth_manager = SpotifyClientCredentials(ClientID, ClientSecret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        albums = sp.search(q, limit=10, offset=0, type='album', market=None)
        response = Response()
        listAlbum = []
        for i in albums['albums']['items']:
            response.data = {
                "idAlbum": i['id'],
                "Name": i['name'],
                "Artist": i['artists'][0]['name'],
                "Image": i['images'][0]['url'],
                "TotalTracks": i['total_tracks'],
                "AverageRating": average_calc(idAlbum=i['id'])
            }
            listAlbum.append(response.data)
        return Response(listAlbum)

class RateAlbum(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        auth_manager = SpotifyClientCredentials(ClientID, ClientSecret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        album = sp.album(album_id=id, market=None)
        if request.user.rated_albums.filter(idAlbum = id).exists() ==True: 
            return Response({"message": "You cannot rate the same album twice"}, status.HTTP_400_BAD_REQUEST)
        albumRated = AlbumRated.objects.create(idAlbum = album['id'], Name=album['name'], Artist=album['artists'][0]['name'], Image = album['images'][0]['url'], TotalTracks=album['total_tracks'], Rating=request.data['rating'])
        albumRated.save()
        request.user.rated_albums.add(albumRated)
        request.user.save()
        serializer = AlbumRatedSerializer(albumRated)
        return Response(serializer.data, status.HTTP_200_OK)

class GetUserRatedAlbums(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        albums = request.user.rated_albums.all()
        serializer = AlbumRatedSerializer(albums, many=True)
        return Response(serializer.data)
