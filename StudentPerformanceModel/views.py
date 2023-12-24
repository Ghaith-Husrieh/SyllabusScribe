from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils.model_loader import student_performance_model
from .serializers import StudentPerformanceSerializer
from decorators.log_decorators import log_api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pandas as pd


@swagger_auto_schema(
    method='POST',
    request_body=StudentPerformanceSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Successful operation',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'model_output': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'performance_index': openapi.Schema(type=openapi.TYPE_NUMBER),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Invalid request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'variable_name': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='This field is required.'
                                )
                            ),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: openapi.Response(
            description='Model currently offline',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default='Model currently offline'
                    ),
                },
            ),
        ),
    },
)
@api_view(['POST'])
@log_api_view
def student_performance_model_query(request):
    if student_performance_model is not None:
        serializer = StudentPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            model_input = pd.DataFrame(
                [[
                    serializer.validated_data['hours_studied'],
                    serializer.validated_data['previous_score'],
                    serializer.validated_data['extracurricular_activities'],
                    serializer.validated_data['sleep_hours'],
                    serializer.validated_data['sample_question_papers_practiced']
                ]],
                columns=['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
                         'Sleep Hours', 'Sample Question Papers Practiced']
            )
            performance_index = student_performance_model.predict(model_input)
            return Response({'model_output': {'performance_index': performance_index[0]}}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
