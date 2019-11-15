from django.urls import path
from .views import (
    overview,
    record_view,
)

urlpatterns = [
    path('', overview, name='overview'),
    path('<int:year>/<int:month>/<int:day>', record_view, name='record'),
]
