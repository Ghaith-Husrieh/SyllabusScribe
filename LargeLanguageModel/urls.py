from django.urls import path

from . import views

urlpatterns = [
    path('query/', views.llm_query, name="llm_query"),
    path('generate-presentation/', views.llm_generate_presentation, name="llm_generate_presentation"),
    path('generate-lesson-plan/', views.llm_generate_lesson_plan, name="llm_generate_lesson_plan"),
    path('generate-quiz/', views.llm_generate_quiz, name="llm_generate_quiz"),
    path('generate-context/', views.llm_generate_context, name="llm_generate_context"),
    path('generate-handout/', views.llm_generate_handout, name="llm_generate_handout")
]
