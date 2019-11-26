from django.forms import formset_factory
from django import forms
from .models import (
    Record,
    CardType,
    Card,
)

# Records FORMS


class NewRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['content', 'score']

# Cards FORMS


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

    TYPE_CHOICES = [('STR', 'Текст'),
                    ('INT', 'Число'),
                    ('LST', 'Лист'),
                    ('BOL', 'Булевое'),
                    ('TAG', 'Тэг')]

    type = forms.ChoiceField(label='Тип',
                             choices=TYPE_CHOICES,
                             initial='STR',
                             required=False)


NewCardQuestionFormset = formset_factory(NewCardQuestionForm, extra=5)


# Answers FORMS

class AnswerStrForm(forms.Form):
    def __init__(self, label=None, *args, **kwargs):
        super(AnswerStrForm, self).__init__(*args, **kwargs)
        self.label = label
        self.fields['value'].label = self.label

    value = forms.CharField()


class AnswerIntForm(forms.Form):
    def __init__(self, label=None, *args, **kwargs):
        super(AnswerIntForm, self).__init__(*args, **kwargs)
        self.label = label
        self.fields['value'].label = self.label

    value = forms.CharField()

    def clean_value(self):
        data = self.cleaned_data['value']
        try:
            int_data = int(data)
        except:
            raise forms.ValidationError('Число должно быть числом, друг')

        return int_data


class AnswerLstForm(forms.Form):
    def __init__(self, label=None, *args, **kwargs):
        super(AnswerLstForm, self).__init__(*args, **kwargs)
        self.label = label
        self.fields['value'].label = self.label

    value = forms.CharField(help_text='Разделяйте элементы списка знаком новой строки (Enter)',
                            widget=forms.Textarea)


class AnswerBolForm(forms.Form):
    def __init__(self, label=None, *args, **kwargs):
        super(AnswerBolForm, self).__init__(*args, **kwargs)
        self.label = label
        self.fields['value'].label = self.label

    value = forms.ChoiceField(choices=(('1', 'Да'), ('0', 'Нет')),
                              widget=forms.RadioSelect)


class AnswerTagForm(forms.Form):
    def __init__(self, label=None, *args, **kwargs):
        super(AnswerTagForm, self).__init__(*args, **kwargs)
        self.label = label
        self.fields['value'].label = self.label

    value = forms.CharField()
