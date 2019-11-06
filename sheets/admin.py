from django.contrib import admin
from .models import (
    Sheet,
    Question,
    Record,
    Answer,
    AnswerInt,
    AnswerStr,
    AnswerTag,
    Tag,
)


class SheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(Sheet, SheetAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'max_value', 'sheet')


admin.site.register(Question, QuestionAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ('sheet', 'date')


admin.site.register(Record, RecordAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'record')


admin.site.register(Answer, AnswerAdmin)

admin.site.register([
    AnswerInt,
    AnswerStr,
    AnswerTag,
    Tag
])
