# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TransactionTestCase
from os.path import join, dirname
from gastos.models import Spending


# Create your tests here.
class ImporterTests(TransactionTestCase):
    def test_xls_importer(self):
        path = join(dirname(__file__), 'test1.xls')
        with open(path, 'rb') as f:
            form = {
                "file": f,
            }

            response = self.client.post('/admin/importer/xls_importer/',
                                        data=form)

        # el archivo deberia procesarse correctamente
        self.assertEqual(response.status_code, 200)

        # deberian haberse guardado 9 objetos
        imported_data = Spending.objects.all()
        self.assertEqual(imported_data.count(), 9)

        # deberia identificarse que uno de los objetos esta duplicado
        duplicates = len(response.context['message']['errors'])
        self.assertEqual(duplicates, 1)
