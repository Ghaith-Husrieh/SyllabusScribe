from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (LessonContext, LessonHandout, LessonPlan,
                     LessonPresentation, LessonQuiz, QuizQA, Subject, User)


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

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        validation_errors = {}
        if User.objects.filter(username=username).exists():
            validation_errors.update({"username": "A user with this username already exists."})
        if User.objects.filter(email=email).exists():
            validation_errors.update({"email": "A user with this email already exists."})
        if validation_errors:
            raise serializers.ValidationError(validation_errors)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'date_joined', 'email', 'bio', 'avatar']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ['user']


class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        exclude = ['user']


class LessonContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContext
        exclude = ['user']


class LessonPresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPresentation
        exclude = ['user']


class LessonHandoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHandout
        exclude = ['user']


class LessonQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonQuiz
        exclude = ['user']


class QuizQASerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQA
        exclude = ['lesson_quiz']


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'avatar']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        validation_errors = {}
        if User.objects.filter(username=username).exists() and self.instance.username != username:
            validation_errors.update({"username": "A user with this username already exists."})
        if User.objects.filter(email=email).exists() and self.instance.email != email:
            validation_errors.update({"email": "A user with this email already exists."})
        if validation_errors:
            raise serializers.ValidationError(validation_errors)

        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
