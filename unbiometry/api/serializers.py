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
                     Student,
                     Presence,
                     FrequencyList)


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

    class Meta:
        model = Class
        fields = ['discipline', 'classe']

    def create(self, validated_data):
        
        discipline = self.context['discipline']
        classe = validated_data['classe']

        # Checking if class does not exist.
        classes = Class.objects.filter(discipline=discipline, classe=classe)
        
        if classes:
            raise ValidationError('Class already exists.')     

        validated_data['discipline'] = discipline
        return Class.objects.create(**validated_data)


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
        fields = ['student', 'classe', 'presences']

    
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

    registration = serializers.CharField(max_length=9)
    date_time = serializers.DateTimeField()
    
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

    def response_presence(self, presence, registration, date_time):

        data = {
            'presence' : presence,
            'registration' : registration,
            'date_time' : date_time
        }

        return data


    def create(self, validated_data):

        registration = validated_data['registration']
        date_time = validated_data['date_time']

        frequency_list = self.get_frequency_list(registration)

        presence = Presence.objects.filter(frequency_list=frequency_list).last()
        
        presence.status = True
        presence.date_time = date_time
        presence.save()

        return self.response_presence(presence, registration, date_time)

        





