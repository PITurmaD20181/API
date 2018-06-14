from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100, blank=False)
    registration = models.CharField(max_length=9, unique=True, blank=False)


class Discipline(models.Model):

    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=50, unique=True, blank=False)


class Class(models.Model):

    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    classe = models.CharField(max_length=10, blank=False)


# Related classes to frequency and student/class relationship registration:

class FrequencyList(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='frequency_lists')
    classe = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')


class Presence(models.Model):

    frequency_list = models.ForeignKey(FrequencyList, on_delete=models.CASCADE, related_name='presences')
    status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'status: %r\ndate_time: %s' % (self.status, str(self.date_time))