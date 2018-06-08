from rest_framework import generics
from .models import Discipline, Class, Student
from .serializers import DisciplineSerializer, ClassSerializer, StudentSerializer


class DisciplineView(generics.ListCreateAPIView):

    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()


class ClassView(generics.ListCreateAPIView):

    serializer_class = ClassSerializer

    # Getting discipline associated with the classes
    def get_discipline(self):
        
        discipline_id = self.kwargs['discipline_id']
        discipline = Discipline.objects.get(pk=discipline_id)

        return discipline

    # Getting list of classses
    def get_queryset(self):
        
        classes = Class.objects.filter(discipline=self.get_discipline())

        return classes

    def get_serializer_context(self):
        context = super(ClassView, self).get_serializer_context()

        context['discipline'] = self.get_discipline()

        return context


class StudentView(generics.ListCreateAPIView):

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
