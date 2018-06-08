from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path(
        'disciplines/',
        views.DisciplineView.as_view(),
        name='disciplines'
    ),
    path(
        'disciplines/<int:discipline_id>',
        views.DisciplineDetailView.as_view(),
        name='discipline_detail'
    ),
    path(
        'disciplines/<int:discipline_id>/classes/',
        views.ClassView.as_view(),
        name='classes'
    ),
    path(
        'classes/<int:class_id>',
        views.ClassDetailView.as_view(),
        name='class_detail'
    ),
    path(
        'students/',
        views.StudentView.as_view(),
        name='students'
    )
]
