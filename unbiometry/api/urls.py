from django.urls import path, include
from . import views

app_name = 'api'


teacher_urls = [
    path(
        '',
        views.TeacherView.as_view(),
        name='teachers'
    ),
    path(
        '<int:teacher_id>/frequency_lists',
        views.TeacherFrequencyListsView.as_view(),
        name='teacher_frequency_lists'
    )
]

students_urls = [
    path(
        '',
        views.StudentView.as_view(),
        name='students'
    ),
    path(
        '<int:student_id>/frequency_lists/',
        views.StudentFrequencyListsView.as_view(),
        name='student_frequency_lists'
    )
]

disciplines_urls = [
    path(
        '',
        views.DisciplineView.as_view(),
        name='disciplines'
    ),
    path(
        '<int:discipline_id>/classes/',
        views.ClassView.as_view(),
        name='classes'
    ),
]

classes_urls = [
    path(
        '<int:class_id>/students/',
        views.StudentsOfClassView.as_view(),
        name = 'students_of_class'
    ),
    path(
        '<int:class_id>/add_student/',
        views.AddStudentInClassView.as_view(),
        name='add_student_in_class'
    )
]

frequency_lists_urls = [
    path(
        'inicialize_presences_list/',
        views.InitializePresencesList.as_view(),
        name='initialize_presence_list'
    ),
    path(
        'add_presence/',
        views.AddPresenceView.as_view(),
        name='add_presence'
    )
]


urlpatterns = [
    path('teachers/', include(teacher_urls)),
    path('students/',include(students_urls)),
    path('disciplines/', include(disciplines_urls)),
    path('classes/', include(classes_urls)),
    path('frequency_lists/', include(frequency_lists_urls))
]
