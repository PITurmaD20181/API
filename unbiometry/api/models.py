from django.db import models


class Discipline(models.Model):

    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=50, blank=False)


class Class(models.Model):

    name = models.CharField(max_length=10, blank=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)


class Student(models.Model):

    name = models.CharField(max_length=100, blank=False)
    registration = models.CharField(max_length=11, blank=False)
    classes = models.ManyToManyField(Class)
