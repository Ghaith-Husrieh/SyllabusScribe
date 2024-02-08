from rest_framework import serializers


class QuerySerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length=1024, required=True)


class GeneratePresentationSerializer(serializers.Serializer):
    num_slides = serializers.IntegerField(required=True)
    topic = serializers.CharField(max_length=128, required=True)
    grade_level = serializers.CharField(max_length=64, required=True)
    unit = serializers.IntegerField(required=False)


class GenerateLessonPlanSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=128, required=True)
    grade_level = serializers.CharField(max_length=64, required=True)
    unit = serializers.IntegerField(required=False)


class GenerateLessonQuizSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=128, required=True)
    grade_level = serializers.CharField(max_length=64, required=True)
    unit = serializers.IntegerField(required=False)


class GenerateLessonContextSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=128, required=True)
    grade_level = serializers.CharField(max_length=64, required=True)
    unit = serializers.IntegerField(required=False)


class GenerateLessonHandoutSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=128, required=True)
    grade_level = serializers.CharField(max_length=64, required=True)
    unit = serializers.IntegerField(required=False)
