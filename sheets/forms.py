from django import forms
from django.forms import ModelForm, formset_factory, ValidationError
from django.utils import timezone

from .models import (
    Sheet,
    Question
)


class NewSheetNameForm(forms.Form):
    name = forms.CharField(label='Choose name for your new sheet')


class NewSheetQuestionForm(forms.Form):
    name = forms.CharField(
        label='Question:',
        required=False,
    )

    TYPE_CHOICES = [
        ('STR', 'String'),
        ('INT', 'Integer'),
        ('TAG', 'Tags'),
    ]

    type = forms.ChoiceField(
        label='Type:',
        choices=TYPE_CHOICES,
        initial='STR',
        required=False,
    )

    max_value = forms.IntegerField(
        label='Max value',
        required=False,
    )


NewSheetQuestionFormset = formset_factory(NewSheetQuestionForm, extra=5)


class NewRecordDateForm(forms.Form):
    date = forms.DateField(
        label='Date:',
        required=True,
        initial=timezone.now()
    )


class NewAnswerForm(forms.Form):

    def __init__(self, type='STR', max_value=None, * args, **kwargs):
        self.label = kwargs.pop('label')
        super(NewAnswerForm, self).__init__(*args, **kwargs)
        self.fields['value'].label = self.label
        self.type = type
        self.max_value = max_value

    value = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data['value']
        if self.type == 'STR' and self.max_value:
            if len(value) > self.max_value:
                raise ValidationError(
                    'Your answer is too long. Restrict yourself in {} characters'.format(self.max_value))
        elif self.type == 'INT':
            try:
                int(value)
            except ValueError:
                raise ValidationError('Your answer must be integer, not string')
            if self.max_value:
                if (int(value) > self.max_value):
                    raise ValidationError('Your answer is too big')
        elif self.type == 'TAG' and self.max_value:
            tags = value.split(', ')
            if len(tags) > self.max_value:
                raise ValidationError('You provided too many tags')
