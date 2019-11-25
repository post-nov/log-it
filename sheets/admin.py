from django.contrib import admin
from .models import (
    Record,
    CardType,
    Card,
    Question,
    Answer,
    AnswerStr,
    AnswerInt,
    AnswerLst,
    AnswerBol,
    AnswerTag,
)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'content'[:10], 'score')


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_archived')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_archived')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('card', 'name', 'type')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'record')


@admin.register(AnswerStr)
class AnswerStrAdmin(admin.ModelAdmin):
    list_display = ('answer', 'value')


@admin.register(AnswerInt)
class AnswerIntAdmin(admin.ModelAdmin):
    list_display = ('answer', 'value')


@admin.register(AnswerLst)
class AnswerLstAdmin(admin.ModelAdmin):
    list_display = ('answer', 'value')


@admin.register(AnswerBol)
class AnswerBolAdmin(admin.ModelAdmin):
    list_display = ('answer', 'value')


# @admin.register(AnswerTag)
# class AnswerTagAdmin(admin.ModelAdmin):
#     list_display = ('answer', 'tag')
