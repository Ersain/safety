from rest_framework.response import Response

from notifications.models import Notification
from .models import QuizCategory, Quiz, Question, QuestionOption, AcceptedAnswer, QuizResult


class QuizResultServices:
    @staticmethod
    def create_accepted_answers(quiz_result: QuizResult, validated_data):
        bulk_list = []
        is_correct_counter = 0

        for item in validated_data:
            if item['option'].is_correct:
                is_correct_counter += 1
            bulk_list.append(
                AcceptedAnswer(
                    quiz_result=quiz_result,
                    question=item['question'],
                    option=item['option'],
                    is_correct=item['option'].is_correct
                )
            )
        AcceptedAnswer.objects.bulk_create(bulk_list)

        quiz_result.score = is_correct_counter
        quiz_result.save()

    @staticmethod
    def populate_db():
        quiz_category = QuizCategory.objects.create(title='Nature')
        quiz = Quiz.objects.create(title='Safety rules on nature #1', category=quiz_category)

        question = Question.objects.create(title='2+2?', quiz=quiz)
        QuestionOption.objects.create(title='2', question=question)
        QuestionOption.objects.create(title='4', question=question, is_correct=True)

        question2 = Question.objects.create(title='3+2?', quiz=quiz)
        QuestionOption.objects.create(title='5', question=question2, is_correct=True)
        QuestionOption.objects.create(title='6', question=question2)

    @staticmethod
    def success_quiz_notification(user, quiz):
        achievement = quiz.achievement
        user.profile.achievements.add(achievement)

        QuizResultServices.unlock_linked_quizzes(quiz)

        notification = Notification.objects.create(
            body=achievement.body,
            user=user
        )
        return {
            'title': notification.title,
            'body': notification.body,
        }

    @staticmethod
    def fail_quiz_notification(user, quiz):
        notification = Notification.objects.create(
            title='Повезет в следующий раз!',
            body=f'Вам не удалось пройти {quiz.title}',
            user=user
        )
        return {
            'title': notification.title,
            'body': notification.body,
        }

    @staticmethod
    def unlock_linked_quizzes(quiz):
        for linked_quiz in quiz.linked_quizzes.iterator():
            linked_quiz.is_active = True
            linked_quiz.save()
