from django.urls import path
from .views import (
    HomeView,
    registration_view,
    logout_view,
    login_view
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration', registration_view, name='registration'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login')

]
