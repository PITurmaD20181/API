from rest_framework import serializers
from .models import Discipline, Class, Student


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


class StudentSerializer(serializers.ModelSerializer):

    classes = ClassSerializer(many=True)

    class Meta:
        model = Student
        fields = ['name', 'registration', 'classes']
