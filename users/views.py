from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import status
from .serializers import UserSerializer
# Create your views here.
def login(request):
    return render(request, 'login.html')

class Login(APIView):
    def post(self, request): 
        email = request.data['email']
        password = request.data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return Response({'message': 'User does not exist'}, status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"message": "Incorrect Password"}, status.HTTP_403_FORBIDDEN)

        token = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        
        response = Response()
        response.set_cookie(key='refresh', value=refresh, httponly=True)

        response.data = {
            'name': user.username,
            'email': user.email,
            'token': str(token),
            'refresh': str(refresh)
        }

        return response
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)