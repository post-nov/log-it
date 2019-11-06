from django.urls import path
from .views import (
    SheetsView,
    sheet_new_view,
    sheet_details_view,
    sheet_delete_view,
    record_new_view,
    record_delete_view,
)

urlpatterns = [
    path('', SheetsView.as_view(), name='sheets'),
    path('new', sheet_new_view, name='sheet_new'),
    path('<str:sheet_name>', sheet_details_view, name='sheet_details'),
    path('<str:sheet_name>/add', record_new_view, name='record_new'),
    path('<str:sheet_name>/delete', sheet_delete_view, name='sheet_delete'),
    path('<str:sheet_name>/<int:record_id>/delete', record_delete_view, name='record_delete'),
]
