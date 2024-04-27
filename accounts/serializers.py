from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.db.models import Q

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    user_type = serializers.CharField(required=False, allow_blank=False)

    def validate(self, data):
        if User.objects.filter( Q(username=data["username"]) | Q(email=data["email"]) ).exists():
            raise serializers.ValidationError("Username or Email is already registered.")
        return data
    
    def create(self, validated_data):
        user = (
            User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"]
            )
        )
        if validated_data["user_type"]:
            group, flag = Group.objects.get_or_create(name=validated_data["user_type"])
            user.groups.add(group)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']