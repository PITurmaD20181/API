from rest_framework import serializers
from .models import Discipline, Class, Student


class DisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = ['name', 'code']


class ClassSerializer(serializers.ModelSerializer):

    discipline = DisciplineSerializer()

    class Meta:
        model = Class
        fields = ['name', 'discipline']


class StudentSerializer(serializers.ModelSerializer):

    classes = ClassSerializer(many=True)

    class Meta:
        model = Student
        fields = ['name', 'registration', 'classes']
