from django.forms import ModelForm

from .models import (
    Record,
)


class NewRecord(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['content', 'score']
