import logging

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import RegistrationForm

logger = logging.Logger(__name__)


class HomeView(ListView):
    template_name = 'general/home.html'

    def get(self, request):
        return render(request, self.template_name)


def registration_view(request):
    template_name = 'user/registration.html'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request, 'Пользователь {} успешно создан'.format(user.username))
            login(request, user)
            return redirect('sheets')

        else:
            return render(
                request,
                template_name,
                {'form': form}
            )

    elif request.method == 'GET':

        return render(
            request,
            template_name,
            {'form': RegistrationForm()}
        )


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'You are now logged in as {}'.format(username))
                return redirect('sheets')
            else:
                messages.error(request, 'Invalid password or username')
        else:
            messages.error(request, 'Invalid password or username')
    return render(
        request,
        'user/login.html',
        {'form': AuthenticationForm}
    )
