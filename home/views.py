from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class HomeView(ListView):
    template_name = 'general/home.html'

    def get(self, request):
        return render(request, self.template_name)


def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect('home')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(
                request,
                'user/registration.html',
                {'form': UserCreationForm}
            )

    return render(
        request,
        'user/registration.html',
        {'form': UserCreationForm}
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
                return redirect('home')
            else:
                messages.error(request, 'Invalid password or username')
        else:
            messages.error(request, 'Invalid password or username')
    return render(
        request,
        'user/login.html',
        {'form': AuthenticationForm}
    )
