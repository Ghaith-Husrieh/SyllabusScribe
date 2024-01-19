from django.contrib import admin

from .models import (LessonContext, LessonHandout, LessonPlan,
                     LessonPresentation, LessonQuiz, QuizQA, Subject, Unit,
                     User)

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
