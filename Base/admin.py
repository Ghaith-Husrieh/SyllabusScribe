from django.contrib import admin
from .models import (
    User,
    Subject,
    Unit,
    LessonPlan,
    LessonContext,
    LessonPresentation,
    LessonHandout,
    LessonQuiz,
    QuizQA
)

# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Unit)
admin.site.register(LessonPlan)
admin.site.register(LessonContext)
admin.site.register(LessonPresentation)
admin.site.register(LessonHandout)
admin.site.register(LessonQuiz)
admin.site.register(QuizQA)
