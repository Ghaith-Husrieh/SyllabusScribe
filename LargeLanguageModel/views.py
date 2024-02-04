from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guidance import assistant, gen, system, user
from guidance.models import LlamaCppChat
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Base.models import LessonContext, LessonPlan, LessonPresentation
from decorators.log_decorators import log_api_view

from .serializers import (GenerateLessonContextSerializer,
                          GenerateLessonPlanSerializer,
                          GenerateLessonQuizSerializer,
                          GeneratePresentationSerializer, QuerySerializer)
from .utils.llama_interface import LlamaInterface
from .utils.presentation_utils import (generate_presentation,
                                       generate_presentation_titles,
                                       generate_title_content)
from .utils.prompt_constants import SystemPrompt
from .utils.quiz_utils import (generate_answer, generate_questions,
                               generate_quiz)
from .utils.text_processing import extract_list
from .utils.toxicity_model_interface import ToxicityModelInterface

# TODO: document 500 and 422 responses for all api views


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
    if isinstance(LLM, LlamaCppChat):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']
            if ToxicityModelInterface.is_loaded():
                is_toxic = ToxicityModelInterface.predict_toxicity(user_input)
                if is_toxic:
                    return Response({'error': 'Toxic or unethical input'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            with system():
                LLM += SystemPrompt.DEFAULT.value
            with user():
                LLM += user_input
            with assistant():
                LLM += gen("model_output", max_tokens=4096, temperature=0.0)
            return Response({'model_output': LLM["model_output"]}, status=status.HTTP_200_OK)
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
    if isinstance(LLM, LlamaCppChat):
        serializer = GeneratePresentationSerializer(data=request.data)
        if serializer.is_valid():
            if ToxicityModelInterface.is_loaded():
                is_toxic = ToxicityModelInterface.predict_toxicity(serializer.validated_data['topic'])
                if is_toxic:
                    return Response({'error': 'Toxic or unethical input'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            presentation_titles = generate_presentation_titles(
                LLM,
                serializer.validated_data['num_slides'],
                serializer.validated_data['topic'],
                serializer.validated_data['grade_level']
            )
            presentation_contents = [generate_title_content(LLM, title) for title in presentation_titles]
            generated_presentation = generate_presentation(
                serializer.validated_data['topic'],
                presentation_titles,
                presentation_contents
            )
            lesson_presentation_object = LessonPresentation.objects.create(
                topic=serializer.validated_data['topic'],
                grade_level=serializer.validated_data['grade_level'],
                generated_file=generated_presentation,
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


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='POST',
    request_body=GenerateLessonPlanSerializer,
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_api_view
def llm_generate_lesson_plan(request):
    LLM = LlamaInterface.create_local_instance()
    if isinstance(LLM, LlamaCppChat):
        serializer = GenerateLessonPlanSerializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.validated_data['topic']
            grade_level = serializer.validated_data['grade_level']
            if ToxicityModelInterface.is_loaded():
                is_toxic = ToxicityModelInterface.predict_toxicity(topic)
                if is_toxic:
                    return Response({'error': 'Toxic or unethical input'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            prompt = f"Generate a lesson plan for the topic '{topic}' for {grade_level} students. It should contain the following: Aim, Objectives, Possible Materials Needed, Lesson Flow, Modeled Practice, Guided Practice, Independent Practice, Common Areas of Struggle, Closure. Use roman numbering and decimal numbering for sub headings"
            with system():
                LLM += SystemPrompt.LESSON_PLAN.value
            with user():
                LLM += prompt
            with assistant():
                LLM += f"Sure, here's a lesson plan for the topic '{topic}' for {grade_level} students:" + \
                    gen('model_output', max_tokens=4096, temperature=0.0)
            lesson_plan_object = LessonPlan.objects.create(
                topic=serializer.validated_data['topic'],
                grade_level=serializer.validated_data['grade_level'],
                content=LLM['model_output'],
                user=request.user
            )
            return Response({'model_output': {
                'message': 'Lesson plan generated successfully',
                'generated_content': lesson_plan_object.content
            }
            }, status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='POST',
    request_body=GenerateLessonQuizSerializer,
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_api_view
def llm_generate_quiz(request):
    LLM = LlamaInterface.create_local_instance()
    if isinstance(LLM, LlamaCppChat):
        serializer = GenerateLessonQuizSerializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.validated_data['topic']
            grade_level = serializer.validated_data['grade_level']
            if ToxicityModelInterface.is_loaded():
                is_toxic = ToxicityModelInterface.predict_toxicity(topic)
                if is_toxic:
                    return Response({'error': 'Toxic or unethical input'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # TODO: Let the user specify the num_questions
            questions_list = generate_questions(LLM, topic, grade_level, 5)
            answers_list = [generate_answer(LLM, question) for question in questions_list]
            generate_quiz(request.user, topic, grade_level, questions_list, answers_list)
            return Response({'model_output': {
                'message': 'Quiz generated successfully'
            }
            }, status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# TODO: Add responses to swagger schema
@swagger_auto_schema(
    method='POST',
    request_body=GenerateLessonContextSerializer,
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_api_view
def llm_generate_context(request):
    LLM = LlamaInterface.create_local_instance()
    if isinstance(LLM, LlamaCppChat):
        serializer = GenerateLessonContextSerializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.validated_data['topic']
            grade_level = serializer.validated_data['grade_level']
            if ToxicityModelInterface.is_loaded():
                is_toxic = ToxicityModelInterface.predict_toxicity(topic)
                if is_toxic:
                    return Response({'error': 'Toxic or unethical input'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            prompt = f"Generate a list of terms that might arise when teaching about the topic of '{topic}' for {grade_level} students."
            with system():
                LLM += SystemPrompt.CONTEXT.value
            with user():
                LLM += prompt
            with assistant():
                LLM += "Here are some terms that might arise when teaching this topic:\n" + \
                    gen('model_output', max_tokens=4096, temperature=0.0)
            extracted_list = extract_list(LLM['model_output'])
            lesson_context_object = LessonContext.objects.create(
                topic=topic,
                grade_level=grade_level,
                content=extracted_list,
                user=request.user
            )
            return Response({'model_output': {
                'message': 'Context generated successfully',
                'generated_content': lesson_context_object.content
            }
            }, status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Model currently offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
