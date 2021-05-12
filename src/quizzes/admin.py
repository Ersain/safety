from django.contrib import admin

from .models import (
    QuizCategory, Quiz, Question, QuestionOption, QuizResult, AcceptedAnswer
)


class QuestionInline(admin.StackedInline):
    model = Question


class QuestionOptionInline(admin.StackedInline):
    model = QuestionOption


@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'size', 'is_active')
    search_fields = ('pk', 'title')
    list_filter = ('is_active',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body',)
    search_fields = ('pk', 'title', 'body')
    autocomplete_fields = ('category',)
    inlines = (QuestionInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body',)
    search_fields = ('pk', 'title', 'body',)
    autocomplete_fields = ('quiz',)
    inlines = (QuestionOptionInline,)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_correct',)
    list_filter = ('is_correct',)
    search_fields = ('pk', 'title', 'question',)
    autocomplete_fields = ('question',)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'quiz', 'score', 'finished_at',)
    readonly_fields = ('finished_at',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AcceptedAnswer)
class AcceptedAnswerAdmin(admin.ModelAdmin):
    list_display = ('is_correct',)
    list_filter = ('is_correct',)

    def has_change_permission(self, request, obj=None):
        return False
