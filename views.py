# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import inspect
from importer import models

# Create your views here.
from .forms import ImportForm


def import_entrypoint_view(request):
    context = configure_context(get_importer_class(request))
    form = configure_form(get_importer_class(request))
    if request.method == 'POST':
        form = configure_form(
            get_importer_class(request),
            request.POST,
            request.FILES
        )
        if form.is_valid():
            context['message'] = handle_uploaded_file(
                get_importer_class(request),
                request
            )
            return render(request, 'importer/index.html', context)
        else:
            context['message'] = 'No valid data.'

    context['form'] = form
    return render(request, 'importer/index.html', context)

def get_importer_class(request):
    # Get from the url the last part, because is the import
    # class to use. Becareful with possible ending slash!
    uri = request.build_absolute_uri('?')
    if uri[-1] == '/':
        uri = uri[:-1]
    class_to_use = uri.rsplit('/', 1)[-1]

    # Look for a class matching name into models, and call to
    # its import method.
    class_importer = None
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and name.lower() == class_to_use.lower():
            class_importer = obj
            break

    return class_importer

def handle_uploaded_file(class_importer, request):
    importer = class_importer()
    return importer.process_file(request)

def configure_context(class_importer):
    context = class_importer.template_context
    return context

def configure_form(class_importer, *args, **kwargs):
    return class_importer.get_form(*args, **kwargs)
