from rest_framework import generics
from .models import Discipline, Class, Student, FrequencyList
from .serializers import (DisciplineSerializer, 
                          ClassSerializer, 
                          StudentSerializer, 
                          FrequencyListSerializer,
                          CreateFrequencyListSerializer,
                          AddPresenceSerializer)


class StudentView(generics.ListCreateAPIView):

    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudentSerializer

    def get_object(self):

        student_id = self.kwargs['student_id']

        try:
            student_object = Student.objects.get(pk=student_id)
        except:
            student_object = None

        return student_object


class DisciplineView(generics.ListCreateAPIView):

    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()


class DisciplineDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = DisciplineSerializer

    def get_object(self):
        
        discipline_id = self.kwargs['discipline_id']

        try:
            discipline = Discipline.objects.get(pk=discipline_id)
        except:
            discipline = None

        return discipline


class ClassView(generics.ListCreateAPIView):

    serializer_class = ClassSerializer

    # Getting discipline associated with the classes
    def get_discipline(self):
        
        discipline_id = self.kwargs['discipline_id']
        
        try:
            discipline = Discipline.objects.get(pk=discipline_id)
        except:
            discipline = None

        return discipline

    # Getting list of classses
    def get_queryset(self):
        
        discipline = self.get_discipline()
        classes = []

        if discipline:
            classes = Class.objects.filter(discipline=discipline)

        return classes

    # Adding discipline in serializer context
    def get_serializer_context(self):
        context = super(ClassView, self).get_serializer_context()

        context['discipline'] = self.get_discipline()

        return context


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ClassSerializer

    def get_object(self):

        class_id = self.kwargs['class_id']

        try:
            class_object = Class.objects.get(pk=class_id)
        except:
            class_object = None

        return class_object

class StudentsOfClassView(generics.ListAPIView):

    serializer_class = StudentSerializer

    def get_class(self):

        class_id = self.kwargs['class_id']
        
        try:
            classe = Class.objects.get(pk=class_id)
        except:
            classe = None
        
        return classe

    def get_queryset(self):

        students = []
        classe = self.get_class()

        if classe:
            relations = FrequencyList.objects.filter(classe=classe)

            for relation in relations:
                students.append(relation.student)
        
        return students


class AddStudentInClassView(generics.CreateAPIView):
    
    serializer_class = CreateFrequencyListSerializer

    def get_class(self):

        class_id = self.kwargs['class_id']

        try:
            classe = Class.objects.get(pk=class_id)
        except:
            classe = None

        return classe


    def get_serializer_context(self):
        
        context = super(AddStudentInClassView, self).get_serializer_context()

        context['class'] = self.get_class()

        return context


class FrequencyListView(generics.ListAPIView):

    serializer_class = FrequencyListSerializer

    def get_student(self):
        student_id = self.kwargs['student_id']
        
        try:
            student = Student.objects.get(pk=student_id)
        except:
            student = None

        return student

    def get_queryset(self):

        student = self.get_student()
        frequecy_lists = []

        if student:
            frequecy_lists = FrequencyList.objects.filter(student=student)

        return frequecy_lists


class FrequencyListDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = FrequencyListSerializer

    def get_object(self):

        frequency_list_id = self.kwargs['frequency_list_id']

        try:
            frequency_list = FrequencyList.objects.get(pk=frequency_list_id)
        except:
            frequency_list = None

        return frequency_list


class AddPresenceView(generics.CreateAPIView):

    serializer_class = AddPresenceSerializer
