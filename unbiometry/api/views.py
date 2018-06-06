from rest_framework import viewsets
from .models import Discipline, Class, Student
from .serializers import DisciplineSerializer, ClassSerializer, StudentSerializer


class DisciplineViewSet(viewsets.ModelViewSet):

    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()


class ClassViewSet(viewsets.ModelViewSet):

    serializer_class = ClassSerializer
    queryset = Class.objects.all()


class StudentViewSet(viewsets.ModelViewSet):

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
