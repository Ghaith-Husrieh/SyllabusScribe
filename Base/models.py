from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(blank=True, default='avatar.svg', upload_to='profile_pictures/')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']


class Subject(models.Model):
    name = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=False)
    lesson_plan = models.OneToOneField('LessonPlan', on_delete=models.CASCADE, null=True)
    lesson_context = models.OneToOneField('LessonContext', on_delete=models.CASCADE, null=True)
    lesson_presentation = models.OneToOneField(
        'LessonPresentation', on_delete=models.CASCADE, null=True)
    lesson_handout = models.OneToOneField('LessonHandout', on_delete=models.CASCADE, null=True)
    lesson_quiz = models.OneToOneField('LessonQuiz', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.name


class LessonPlan(models.Model):
    topic = models.CharField(max_length=128)
    grade_level = models.CharField(max_length=64)
    content = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.topic


class LessonContext(models.Model):
    topic = models.CharField(max_length=128)
    grade_level = models.CharField(max_length=64)
    content = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.topic


class LessonPresentation(models.Model):
    topic = models.CharField(max_length=128)
    grade_level = models.CharField(max_length=64)
    generated_file = models.FileField(null=False, blank=False, upload_to='presentations/')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.topic


class LessonHandout(models.Model):
    topic = models.CharField(max_length=128)
    grade_level = models.CharField(max_length=64)
    content = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.topic


class LessonQuiz(models.Model):
    topic = models.CharField(max_length=128)
    grade_level = models.CharField(max_length=64)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return self.topic


class QuizQA(models.Model):
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    lesson_quiz = models.ForeignKey('LessonQuiz', on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_date', '-created_date']

    def __str__(self) -> str:
        return f'{self.lesson_quiz.topic} - QA'
