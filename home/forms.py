from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):

    username = forms.RegexField(
        label=("Имя пользователя"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=("Обязательное. 30 знаков или меньше. Только буквы, цифры и @/./+/-/_"),
        error_messages={
            'invalid': ("Имя может содержать только буквы, цифры и @/./+/-/_")
        }
    )

    password1 = forms.CharField(label=("Пароль"),
                                widget=forms.PasswordInput)

    password2 = forms.CharField(label=("Подтверждение пароля"),
                                widget=forms.PasswordInput,
                                help_text=("Введите пароль еще раз.")
                                )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(("Пользователь с таким именем уже существует"))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(("Пароли не совпадают"))
        return password2
