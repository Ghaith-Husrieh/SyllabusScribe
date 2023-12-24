from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from guidance import models, system, user, assistant, gen
from .utils.model_loader import llama2
from .utils.presentation_utils import generate_presentation_titles, generate_title_content, generate_presentation
from .utils.prompt_constants import DEFAULT_SYSTEM_PROMPT
from .serializers import QuerySerializer, GeneratePresentationSerializer
from decorators.log_decorators import log_api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='POST',
    request_body=QuerySerializer,
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
    },
)
@api_view(['POST'])
@log_api_view
def llm_query(request):
    if llama2 is not None:
        LLM = models.LlamaCppChat(model=llama2)
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
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Successful operation',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'model_output': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default="Successfully generated 'topic_name.pptx'"
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
    },
)
@api_view(['POST'])
@log_api_view
def llm_generate_presentation(request):
    if llama2 is not None:
        LLM = models.LlamaCppChat(model=llama2)
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
            generate_presentation(
                serializer.validated_data['topic'],
                presentation_titles,
                presentation_contents
            )
            return Response({'model_output': f"Successfully generated '{serializer.validated_data['topic']}.pptx'"})
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
