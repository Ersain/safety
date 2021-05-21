from django.db import models


class QuizCategory(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    size = models.IntegerField(default=1)
    icon = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quiz Categories'


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    pass_mark = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
        to='quizzes.QuizCategory',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='quizzes'
    )
    achievement = models.OneToOneField(
        to='notifications.Achievement',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)

    quiz = models.ForeignKey(
        to='quizzes.Quiz',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='questions'
    )

    def __str__(self):
        return self.title


class QuestionOption(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        to='quizzes.Question',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='options'
    )

    def __str__(self):
        return f'{self.pk} - {self.title}'


class QuizResult(models.Model):
    score = models.PositiveIntegerField(default=0)
    finished_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        to='users.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='quiz_results'
    )
    quiz = models.ForeignKey(
        to='quizzes.Quiz',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.user.email}, {self.quiz.title}'


class AcceptedAnswer(models.Model):
    """
    Accepted answer from a `user`
    """
    is_correct = models.BooleanField(default=False)

    quiz_result = models.ForeignKey(
        to='quizzes.QuizResult',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='accepted_answers'
    )
    question = models.ForeignKey(
        to='quizzes.Question',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    option = models.ForeignKey(
        to='quizzes.QuestionOption',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.question}'
