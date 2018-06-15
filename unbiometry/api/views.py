# Django
from django.core import serializers
from django.core.exceptions import (ObjectDoesNotExist, 
                                    ValidationError)

# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

# Application
from . import constants
from .models import (Discipline, 
                     Class,
                     Teacher,
                     Student, 
                     FrequencyList, 
                     Presence)
from .serializers import (DisciplineSerializer, 
                          ClassSerializer,
                          TeacherSerializer, 
                          StudentSerializer, 
                          FrequencyListSerializer,
                          CreateFrequencyListSerializer,
                          AddPresenceSerializer)


class TeacherView(generics.ListCreateAPIView):

    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeacherFrequencyListsView(APIView):

    def get_teacher(self):
        teacher_id = self.kwargs['teacher_id']
        
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
        except:
            teacher = None

        return teacher

    def get_classes(self):

        teacher = self.get_teacher()
        classes = Class.objects.filter(teacher=teacher)

        return classes

    def build_presences_list(self, frequency_list):

        presences_list = []

        for elem in frequency_list:

            presences = Presence.objects.filter(frequency_list=elem).values('status', 'date_time')

            elem_data = {
                'student_name' : elem.student.name,
                'student_registration' : elem.student.registration,
                'frequency' : elem.frequency,
                'presences' : presences
            }

            presences_list.append(elem_data)
        
        return presences_list

    def get(self, request, *args, **kwargs):

        frequecy_lists = []

        classes = self.get_classes()

        for classe in classes:
            frequency_list = FrequencyList.objects.filter(classe=classe)
            frequecy_lists.append(
                {
                    'discipline_name' : classe.discipline.name,
                    'discipline_code' : classe.discipline.code,
                    'classe' : classe.classe,
                    'presences_list' : self.build_presences_list(frequency_list)
                })

        return Response(frequecy_lists)


class StudentView(generics.ListCreateAPIView):

    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentFrequencyListsView(generics.ListAPIView):

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


class DisciplineView(generics.ListCreateAPIView):

    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()


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


class InitializePresencesList(APIView):

    def get_classe(self):

        discipline_code = constants.PI_CODE
        class_name = constants.CLASS_NAME

        try:
            discipline = Discipline.objects.filter(code=discipline_code)[0]
            classe = Class.objects.filter(discipline=discipline, classe=class_name)[0]
        except:
            raise ObjectDoesNotExist('Error trying to get discipline and class.')

        return classe

    
    def update_frequency(self, frequency_list):

        presences = Presence.objects.filter(frequency_list=frequency_list)
        presences_true = [elem for elem in presences if elem.status == True]

        total_presences = len(presences)
        total_presences_true = len(presences_true)
     
        if total_presences_true != 0:
            result = round(float((total_presences_true*100)/total_presences), 2)
        else:
            result = 0

        frequency_list.frequency = result
        frequency_list.save()


    def initialize_presences_list(self):

        frequency_lists = FrequencyList.objects.filter(classe=self.get_classe())
        presences = []

        for frequency_list in frequency_lists:
            presence = Presence.objects.create(frequency_list=frequency_list)
            presences.append(presence)
            self.update_frequency(frequency_list)

        return presences

    def get(self, request, format=None):

        presences = self.initialize_presences_list()

        data = serializers.serialize("json", presences)

        return Response(data)


class AddPresenceView(generics.CreateAPIView):

    serializer_class = AddPresenceSerializer
