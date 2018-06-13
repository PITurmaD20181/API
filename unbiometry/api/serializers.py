from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
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
        fields = ['name', 'discipline']

    def create(self, validated_data):
        
        discipline = self.context['discipline']
        name = validated_data['name']

        # Checking if class does not exist.
        classes = Class.objects.filter(discipline=discipline, name=name)
        
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






