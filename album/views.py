from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .helper import Album
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from spotipy.oauth2 import SpotifyClientCredentials
from .models import AlbumRated
import spotipy
import json

ClientID = "a0f03799e3bd4048bfbbcfc4e0850b6d"
ClientSecret = "27ff31beecaa44628a7f43dd1ab91335"

class GetAlbum(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='album_search.html'
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
                "TotalTracks": i['total_tracks']
            }
            listAlbum.append(response.data)
        print(listAlbum)
        return Response({'albums': listAlbum})

class RateAlbum(APIView):
    def post(self, request, id):
        auth_manager = SpotifyClientCredentials(ClientID, ClientSecret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        album = sp.album(album_id=id, market=None)
        albumRated = AlbumRated.objects.create(idAlbum = album['id'], Name=album['name'], Artist=album['artists'][0]['name'], Image = album['images'][0]['url'], TotalTracks=album['total_tracks'], Rating=10)
        albumRated.save()
        return Response(AlbumRated.objects.latest('-id'))