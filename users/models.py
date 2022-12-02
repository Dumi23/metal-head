from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from album.models import AlbumRated
# Create your models here.
class User(AbstractUser):    
    STATUS =(
            ('Online', 'Online'),
            ('Offline', 'Offline'),
            ('Away', 'Away'),
            ('Busy', 'Busy'),
            )
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=500, validators=[MinLengthValidator(8)])
    profile_pic = models.ImageField(upload_to="profile_pics", null=True)
    rated_albums = models.ManyToManyField(AlbumRated)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']