# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .forms import ImportForm

class ImporterBase(models.Model):
    class Meta:
        managed = False

    template_context = {
        'title_page': 'Import file app',
        'title': 'Default import example',
        'button': 'Import me!'
    }

    def process_file(self, request):
        file_path = self.save_uploaded_file(request.FILES['file'])
        return "The file {} will be processed".format(file_path)

    @staticmethod
    def get_form(*args, **kwargs):
        return ImportForm(*args, **kwargs)

    @staticmethod
    def save_uploaded_file(file_uploaded):
        temp_file = 'uploaded_file.tmp'
        with open(temp_file, 'wb+') as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)

        return temp_file

# Create your models import here.
class Example_Importer(ImporterBase):
    class Meta:
        managed = False
        verbose_name = 'Default importer'


