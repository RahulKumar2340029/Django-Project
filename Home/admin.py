from django.contrib import admin
from .models import Task
# models not seen without registering

# Register your models here.
admin.site.register(Task)