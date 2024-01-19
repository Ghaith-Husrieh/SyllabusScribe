from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from decorators.log_decorators import log_api_view

from .models import (LessonContext, LessonHandout, LessonPlan,
                     LessonPresentation, LessonQuiz, Subject)
from .serializers import (LessonContextSerializer, LessonHandoutSerializer,
                          LessonPlanSerializer, LessonPresentationSerializer,
                          LessonQuizSerializer, QuizQASerializer,
                          SignUpSerializer, SubjectSerializer, UserSerializer)


@swagger_auto_schema(
    method='POST',
    request_body=SignUpSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Successful operation',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "username": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "bio": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
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
    }
)
@api_view(['POST'])
@permission_classes((AllowAny,))
@log_api_view
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
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
            description='Successful response',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "bio": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        "avatar": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Unauthorized",
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
        )
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_personal_info(request):
    serialized_object = UserSerializer(request.user)
    return Response(serialized_object.data, status.HTTP_200_OK)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_user_subjects(request):
    try:
        subjects = Subject.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if subjects:
        serialized_object = SubjectSerializer(subjects, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@log_api_view
def get_user_lesson_plans(request):
    try:
        lesson_plans = LessonPlan.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lesson_plans:
        serialized_object = LessonPlanSerializer(lesson_plans, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_user_lesson_contexts(request):
    try:
        lesson_contexts = LessonContext.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lesson_contexts:
        serialized_object = LessonContextSerializer(lesson_contexts, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_user_lesson_presentations(request):
    try:
        lesson_presentations = LessonPresentation.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lesson_presentations:
        serialized_object = LessonPresentationSerializer(lesson_presentations, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_user_lesson_handouts(request):
    try:
        lesson_handouts = LessonHandout.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lesson_handouts:
        serialized_object = LessonHandoutSerializer(lesson_handouts, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='GET',
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
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@log_api_view
def get_user_lesson_quizzes(request):
    try:
        lesson_quizzes = LessonQuiz.objects.filter(user=request.user)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lesson_quizzes:
        serialized_data = []
        for lesson_quiz in lesson_quizzes:
            serialized_lesson_quiz = LessonQuizSerializer(lesson_quiz).data

            try:
                lesson_quiz_qa = lesson_quiz.quizqa_set.all()
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serialized_quiz_qas = QuizQASerializer(lesson_quiz_qa, many=True).data

            serialized_lesson_quiz['quiz_qas'] = serialized_quiz_qas
            serialized_data.append(serialized_lesson_quiz)

        return Response(serialized_data, status.HTTP_200_OK)
    else:
        return Response({}, status.HTTP_204_NO_CONTENT)
