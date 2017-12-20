# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import inspect
import models

# Register your models here.

class ImporterAdministration(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

# Import all classes in models.py in order to make it
# appear at the main admin interface.
for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        admin.site.register(obj, ImporterAdministration)

