from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from .validators import validate_file_extension, file_size
import os

class ProgramCategory(models.Model):
    category = models.CharField(max_length=128)
    def __str__(self):
        return self.category

class Program(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    upload = models.FileField(upload_to='documents/', validators=[validate_file_extension, file_size])
    date = models.DateField(auto_now=True)
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE)
    is_public = models.BooleanField()
    def clean(self, *args, **kwargs):
        super(Program, self).clean(*args, **kwargs)
        if not self.upload:
            raise ValidationError('Please provide a file')

