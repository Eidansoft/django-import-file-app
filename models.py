# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from .forms import ImportForm
from importer.ProcesaExcel import ProcesaExcel, Celda
from gastos.models import Spending


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
        data = excel_procesor.get_excel_data()

        import ipdb; ipdb.set_trace(context=21)
        for movement in data:
            the_date = datetime.strptime(
                movement.get(u'FECHA VALOR').value,
                '%d/%m/%Y'
            )
            obj = Spending.objects.create(
                concept = movement.get(u'DESCRIPCI\xd3N').value,
                date = the_date,
                amount = movement.get(u'IMPORTE (\u20ac)').value
            )
            pass



