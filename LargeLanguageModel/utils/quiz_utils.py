from guidance import assistant, gen, models, system, user

from Base.models import LessonQuiz, QuizQA
from decorators.log_decorators import log_function

from .prompt_constants import SystemPrompt


@log_function(log_result=False)
def generate_questions(model, topic, grade_level, num_questions):
    prompt = f"Generate {num_questions} MCQ questions for the topic {topic} for {grade_level} students. Don't answer them. Make sure to separate each question from the other using a line break."
    with system():
        model += SystemPrompt.QUIZ.value
    with user():
        model += prompt
    with assistant():
        model += f"Here are {num_questions} multiple-choice questions on the topic of {topic} that are suitable for {grade_level} students:\n" + \
            gen('output', max_tokens=4096, temperature=0.0)
    return model['output'].split("\n\n")


@log_function(log_result=False)
def generate_answer(model, question):
    prompt = f"Answer the following questions MCQ question: {question}. Don't explain the answer. Only Choose one of the given options."
    with system():
        model += SystemPrompt.QUIZ.value
    with user():
        model += prompt
    with assistant():
        model += "Great, I'd be happy to help! The answer to the question is:\n" + \
            gen('output', max_tokens=4096, temperature=0.0, stop='\n')
    return model['output']


@log_function(log_result=False)
def generate_quiz(user, topic, grade_level, questions_list, answers_list):
    quiz = LessonQuiz.objects.create(
        topic=topic,
        grade_level=grade_level,
        user=user
    )
    for question, answer in zip(questions_list, answers_list):
        QuizQA.objects.create(
            question=question,
            answer=answer,
            lesson_quiz=quiz
        )
