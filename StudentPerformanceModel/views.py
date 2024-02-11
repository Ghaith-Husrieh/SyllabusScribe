from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from decorators.log_decorators import log_api_view

from .serializers import (PerformanceIndexSerializer,
                          StudentPerformanceSerializer)
from .utils.student_performance_model_interface import \
    StudentPerformanceModelInterface


@swagger_auto_schema(
    method='POST',
    request_body=StudentPerformanceSerializer,
    manual_parameters=[
        openapi.Parameter(
            name="Authorization",
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description="Bearer token",
            required=True,
            default="Bearer 'your_access_token'",
        ),
    ],
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
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Unauthorized',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token_class': openapi.Schema(type=openapi.TYPE_STRING),
                                'token_type': openapi.Schema(type=openapi.TYPE_STRING),
                                'message': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description='Internal Server Error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default='Something went wrong'
                    )
                },
            ),
        )
    },
)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@log_api_view
def student_performance_model_query(request):
    if StudentPerformanceModelInterface.is_loaded():
        serializer = StudentPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            performance_index = StudentPerformanceModelInterface.predict_performance_index(
                serializer.validated_data['hours_studied'],
                serializer.validated_data['previous_score'],
                serializer.validated_data['extracurricular_activities'],
                serializer.validated_data['sleep_hours'],
                serializer.validated_data['sample_question_papers_practiced']
            )
            output_serializer = PerformanceIndexSerializer(data={'performance_index': performance_index[0]})
            if output_serializer.is_valid():
                return Response({'model_output': {'performance_index': output_serializer.validated_data['performance_index']}}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
