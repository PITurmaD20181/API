# Standard Library
import json

# Django
from django.core.exceptions import (ObjectDoesNotExist, 
                                    ValidationError)

# Rest Framework                                    
from rest_framework import serializers

# Application
from . import constants
from .models import (Discipline, 
                     Class,
                     Teacher,
                     Student,
                     Presence,
                     FrequencyList)


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['name', 'email']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['name', 'registration']


class DisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = ['name', 'code']


class ClassSerializer(serializers.ModelSerializer):

    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    teacher_email = serializers.EmailField(max_length=100, write_only=True)

    class Meta:
        model = Class
        fields = ['discipline', 'classe', 'teacher', 'teacher_email']

    def get_teacher(self, validated_data):

        teacher_email = validated_data['teacher_email']

        try:
            teacher = Teacher.objects.filter(email=teacher_email)[0]
        except:
            raise ObjectDoesNotExist('Teacher does not exist.')

        return teacher

    def create(self, validated_data):
        
        discipline = self.context['discipline']
        classe = validated_data['classe']

        # Checking if class does not exist.
        classes = Class.objects.filter(discipline=discipline, classe=classe)
        
        if classes:
            raise ValidationError('Class already exists.')

        teacher = self.get_teacher(validated_data)

        return Class.objects.create(discipline=discipline,
                                    classe=classe,
                                    teacher=teacher)


class PresenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presence
        fields = ['status', 'date_time']


class FrequencyListSerializer(serializers.ModelSerializer):

    student = StudentSerializer(read_only=True)
    classe = ClassSerializer(read_only=True)
    presences = PresenceSerializer(many=True, read_only=True)

    class Meta:
        model = FrequencyList
        fields = ['student', 'classe', 'frequency', 'presences']

    
class CreateFrequencyListSerializer(serializers.Serializer):

    student = serializers.CharField(max_length=9)

    def get_student(self, registration, classe):

        # Checking if student exists.
        try:
            student = Student.objects.get(registration=registration)
        except:
            raise ObjectDoesNotExist('Student not found.')

        # Checking if student is not already added in the class.
        frequency_lists = FrequencyList.objects.filter(classe=classe, student=student)

        if frequency_lists:
            raise ValidationError('Student already added.')

        return student


    def create(self, validated_data):

        registration = validated_data['student']
        
        classe = self.context['class']
        student = self.get_student(registration, classe)

        return FrequencyList.objects.create(student=student, classe=classe)


class AddPresenceSerializer(serializers.Serializer):

    presence = PresenceSerializer(read_only=True)

    registration = serializers.CharField(max_length=9, write_only=True)
    date_time = serializers.DateTimeField(write_only=True)
    
    def get_class(self):

        discipline_code = constants.PI_CODE
        class_name = constants.CLASS_NAME

        try:
            discipline = Discipline.objects.get(code=discipline_code)
            classe = Class.objects.get(discipline=discipline, classe=class_name)
        except:
            raise ObjectDoesNotExist('Error trying to get discipline and class.')

        return classe

    def get_student(self, registration):

        try:
            student = Student.objects.get(registration=registration)
        except:
            raise ObjectDoesNotExist('Student does not exist.')

        return student

    def get_frequency_list(self, registration):

        student = self.get_student(registration)
        classe = self.get_class()

        try:
            frequency_list = FrequencyList.objects.get(student=student, classe=classe)
        except:
            raise ObjectDoesNotExist("""Student is not added in the class.\n
                                        Frequency list does not exist."""
                                    )

        return frequency_list

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

    def create(self, validated_data):

        registration = validated_data['registration']
        date_time = validated_data['date_time']

        frequency_list = self.get_frequency_list(registration)

        presence = Presence.objects.filter(frequency_list=frequency_list).last()
        
        presence.status = True
        presence.date_time = date_time
        presence.save()

        self.update_frequency(frequency_list)

        return presence

        





