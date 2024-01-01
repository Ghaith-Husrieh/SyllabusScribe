from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'bio', 'avatar']

    def create(self, validated_data):
        default_avatar = User._meta.get_field('avatar').get_default()
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'].lower(),
            bio=validated_data.get('bio', None),
            avatar=validated_data.get('avatar', default_avatar)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
