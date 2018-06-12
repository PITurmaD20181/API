from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100, blank=False)
    registration = models.CharField(max_length=11, blank=False)


class Discipline(models.Model):

    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=50, blank=False)


class Class(models.Model):

    name = models.CharField(max_length=10, blank=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)


# Related classes to frequency and student/class relationship registration:


class Presence(models.Model):

    status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)


class FrequencyList(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='frequency_lists')
    classe = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    presences = models.ManyToManyField(Presence)