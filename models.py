# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Xls(models.Model):
    class Meta:
        managed = False

    def process_file(self, file_path):
        return "The file {} will be processed".format(file_path)

class Mdb(models.Model):
    class Meta:
        managed = False

