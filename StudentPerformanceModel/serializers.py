from rest_framework import serializers


class StudentPerformanceSerializer(serializers.Serializer):
    hours_studied = serializers.IntegerField(required=True)
    previous_score = serializers.IntegerField(required=True)
    extracurricular_activities = serializers.IntegerField(required=True)
    sleep_hours = serializers.IntegerField(required=True)
    sample_question_papers_practiced = serializers.IntegerField(required=True)


class PerformanceIndexSerializer(serializers.Serializer):
    performance_index = serializers.FloatField(required=True)

    def validate(self, data):
        performance_index = data.get('performance_index')

        if performance_index > 100:
            data['performance_index'] = 100
        elif performance_index < 0:
            data['performance_index'] = 0

        return data
