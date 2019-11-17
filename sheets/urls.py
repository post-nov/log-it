from django.urls import path
from .views import (
    overview,
    record_view,
    cards_view,
    new_card_type_view,
    new_card_view,
)

urlpatterns = [
    path('', overview, name='overview'),
    path('<int:year>/<int:month>/<int:day>', record_view, name='record'),
    path('cards/', cards_view, name='cards'),
    path('cards/new/', new_card_type_view, name='new_card_type'),
    path('cards/<str:card_type>/new/', new_card_view, name='new_card'),
]
