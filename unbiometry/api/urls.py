from django.urls import path, include
from . import views

app_name = 'api'

students_urls = [
    path(
        '',
        views.StudentView.as_view(),
        name='students'
    ),
    path(
        '<int:student_id>/',
        views.StudentDetailView.as_view(),
        name='student_detail'
    ),
    path(
        '<int:student_id>/frequency_lists/',
        views.FrequencyListView.as_view(),
        name='frequency_lists'
    ),
]

disciplines_urls = [
    path(
        '',
        views.DisciplineView.as_view(),
        name='disciplines'
    ),
    path(
        '<int:discipline_id>/',
        views.DisciplineDetailView.as_view(),
        name='discipline_detail'
    ),
    path(
        '<int:discipline_id>/classes/',
        views.ClassView.as_view(),
        name='classes'
    ),
]

classes_urls = [
    path(
        '<int:class_id>/',
        views.ClassDetailView.as_view(),
        name='class_detail'
    ),
    # path(
    #     '<int:class_id>/students/',
    #     views.StudentsOfClassView.as_view(),
    #     name='students_of_class'
    # )
]

frequency_lists_urls = [
    path(
        '<int:frequency_list_id>/',
        views.FrequencyListDetailView.as_view(),
        name='frequency_list_detail'
    )
]


urlpatterns = [
    path('students/',include(students_urls)),
    path('disciplines/', include(disciplines_urls)),
    path('classes/', include(classes_urls)),
    path('frequency_lists/', include(frequency_lists_urls))
]
