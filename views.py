# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import inspect
import models

# Create your views here.
from .forms import ImportForm


def import_entrypoint_view(request):

    context = {}
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = save_uploaded_file(request.FILES['file'])
            context['message'] = handle_uploaded_file(request, file_path)
            return render(request, 'importer/index.html', context)
        else:
            context['message'] = 'No valid data.'

    form = ImportForm()
    context['form'] = form
    return render(request, 'importer/index.html', context)

def save_uploaded_file(file_uploaded):
    temp_file = 'uploaded_file.tmp'
    with open(temp_file, 'wb+') as destination:
        for chunk in file_uploaded.chunks():
            destination.write(chunk)

    return temp_file

def handle_uploaded_file(request, file_path):
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

    if class_importer:
        importer = class_importer()
        return importer.process_file(file_path)
    else:
        return 'The import class for {} is not properly configured'.format(class_to_use)
