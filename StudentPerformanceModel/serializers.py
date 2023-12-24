from rest_framework import serializers


class StudentPerformanceSerializer(serializers.Serializer):
    hours_studied = serializers.IntegerField(required=True)
    previous_score = serializers.IntegerField(required=True)
    extracurricular_activities = serializers.IntegerField(required=True)
    sleep_hours = serializers.IntegerField(required=True)
    sample_question_papers_practiced = serializers.IntegerField(required=True)
