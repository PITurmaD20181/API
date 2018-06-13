from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Discipline)
admin.site.register(models.Class)
admin.site.register(models.Presence)
admin.site.register(models.FrequencyList)
