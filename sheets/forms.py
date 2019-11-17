from django.forms import formset_factory
from django import forms
from .models import (
    Record,
    CardType,
    Card,
)


class NewRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['content', 'score']


class NewCardTypeForm(forms.ModelForm):
    class Meta:
        model = CardType
        fields = ['name', 'color']


class NewCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name']


class NewCardQuestionForm(forms.Form):
    name = forms.CharField(label='Поле', required=False)

    TYPE_CHOICES = [('STR', 'Text'),
                    ('INT', 'Number'),
                    ('LST', 'List'),
                    ('BOL', 'Boolean'),
                    ('TAG', 'Tag')]

    type = forms.ChoiceField(label='Тип',
                             choices=TYPE_CHOICES,
                             initial='STR',
                             required=False)


NewCardQuestionFormset = formset_factory(NewCardQuestionForm, extra=5)
