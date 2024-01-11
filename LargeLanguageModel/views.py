from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from guidance import system, user, assistant, gen
from .utils.presentation_utils import generate_presentation_titles, generate_title_content, generate_presentation
from .utils.prompt_constants import DEFAULT_SYSTEM_PROMPT
from .utils.llama_interface import LlamaInterface
from .serializers import QuerySerializer, GeneratePresentationSerializer
from decorators.log_decorators import log_api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Base.models import LessonPresentation
from django.core.files.base import ContentFile


@swagger_auto_schema(
    method='POST',
    request_body=QuerySerializer,
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
                    'model_output': openapi.Schema(type=openapi.TYPE_STRING)
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
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@log_api_view
def llm_query(request):
    LLM = LlamaInterface.create_local_instance()
    if LLM is not None:
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']
            with system():
                LLM += DEFAULT_SYSTEM_PROMPT
            with user():
                LLM += user_input
            with assistant():
                LLM += gen("model_output", max_tokens=4096)
            model_output = LLM["model_output"]
            return Response({'model_output': model_output}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@swagger_auto_schema(
    method='POST',
    request_body=GeneratePresentationSerializer,
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
        status.HTTP_201_CREATED: openapi.Response(
            description='Successful operation',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'model_output': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING),
                            'file_path': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
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
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@log_api_view
def llm_generate_presentation(request):
    LLM = LlamaInterface.create_local_instance()
    if LLM is not None:
        serializer = GeneratePresentationSerializer(data=request.data)
        if serializer.is_valid():
            presentation_titles = generate_presentation_titles(
                LLM,
                serializer.validated_data['num_slides'],
                serializer.validated_data['topic'],
                serializer.validated_data['grade_level']
            )
            presentation_contents = [generate_title_content(LLM, title)
                                     for title in presentation_titles]
            generated_presentation = generate_presentation(
                serializer.validated_data['topic'],
                presentation_titles,
                presentation_contents
            )
            lesson_presentation_object = LessonPresentation.objects.create(
                topic=serializer.validated_data['topic'],
                grade_level=serializer.validated_data['grade_level'],
                generated_file=ContentFile(generated_presentation.getvalue(),
                                           name=f"{serializer.validated_data['topic']}.pptx"),
                user=request.user
            )
            return Response({'model_output': {
                'message': 'Presentation generated successfully',
                'file_path': f'{lesson_presentation_object.generated_file}'
            }
            }, status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
