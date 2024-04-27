from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.viewsets import ModelViewSet

class RegisterUser(APIView):
    target_object = {
        "app" : "auth",
        "model" : "user",
        "object_type" : "user"
    }

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "message" : serializer.errors 
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({
            "message" : "User saved successfully"
        }, status=status.HTTP_200_OK)
    
class LoginUser(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "message" : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data
        user = authenticate(username=user["username"], password=user["password"])
        if user:
            token, flag = Token.objects.get_or_create(user=user)
            return Response({
                "token" : str(token)
            }, status=status.HTTP_200_OK)
        return Response({
            "message" : "Invalid Credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
class UsersList(APIView):
    def get(self, request):
        users = User.objects.all()
        users = UserSerializer(users, many=True).data
        return Response(users)

class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & (IsSuperuser | IsOwner)]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)