from django.core.exceptions import ObjectDoesNotExist
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

    def create(self, validated_data):

        student = validated_data['student']

        try:
            student_object = Student.objects.get(registration=student)
        except:
            raise ObjectDoesNotExist('Student not found.')

        classe = self.context['class']
        frequecy_list = FrequencyList.objects.create(student=student_object, classe=classe)

        return frequecy_list






