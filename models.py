# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models import here.
class Example_Importer(models.Model):
    class Meta:
        managed = False
        verbose_name = 'my test'

    template_context = {
        'title_page': 'Import file app',
        'title': 'Default import example',
        'button': 'Import me!'
    }

    def process_file(self, file_path):
        
        return "The file {} will be processed".format(file_path)

