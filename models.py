# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.utils import IntegrityError
from datetime import datetime
from .forms import ImportForm
from importer.ProcesaExcel import ProcesaExcel, Celda
from gastos.models import Spending, Tag


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
class Xls_Importer(ImporterBase):
    class Meta:
        managed = False
        verbose_name = 'Excel (xls)'

    def process_file(self, request):
        file_path = self.save_uploaded_file(request.FILES['file'])
        excel_procesor = ProcesaExcel(
            file_path,
            Celda(5, 0),
            Celda(5, 5)
        )

        tag = request.POST['tag_name']
        existing_tag, created = Tag.objects.get_or_create(name=tag)

        data = excel_procesor.get_excel_data()

        errors = []
        for movement in data:
            the_date = datetime.strptime(
                movement.get(u'FECHA VALOR').value,
                '%d/%m/%Y'
            )

            spend = Spending()
            spend.concept = movement.get(u'DESCRIPCI\xd3N').value
            spend.date = the_date
            spend.amount = movement.get(u'IMPORTE (\u20ac)').value

            try:
                spend.save()
            except IntegrityError:
                errors.append(spend)
            else:
                spend.tags.set([existing_tag])
                spend.save()

        return {'msg': 'Data saved!', 'errors': errors}
