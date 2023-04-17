from django.shortcuts import render

from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer
from .models import MyUser as User
from rest_framework.decorators import api_view


class UserRegister(generics.GenericAPIView):
    def post(self, request, *args,  **kwargs):
        get_user_model().objects.create_user(request.data['email'], request.data['password'])
        return Response({
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
    
class AdminRegister(generics.GenericAPIView):
    def post(self, request, *args,  **kwargs):
        get_user_model().objects.create_superuser(request.data['email'], request.data['password'])
        return Response({
            "message": "Admin Created Successfully.  Now perform Login to get your token",
        })
    
class AuthenticationCheck(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'User is authenticated'}
        return Response(content)
    
class AdminAuthenticationCheck(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request):
        content = {'message': 'Admin is authenticated'}
        return Response(content)
    



# Create your views here.

@api_view(['GET'])
def user_list(request, ):
    users = User.objects.all().order_by('email')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)
