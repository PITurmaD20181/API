from django.urls import path, include
from .views import DisciplineView, ClassView, StudentView

app_name = 'api'

urlpatterns = [
    path(
        'disciplines/',
        DisciplineView.as_view(),
    ),
    path(
        'disciplines/<int:discipline_id>/classes/',
        ClassView.as_view(),
    )
]
