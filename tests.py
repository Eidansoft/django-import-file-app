# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TransactionTestCase
from os.path import join, dirname
from gastos.models import Spending, Tag


# Create your tests here.
class ImporterTests(TransactionTestCase):
    def test_xls_importer_with_no_tag(self):
        path = join(dirname(__file__), 'test1.xls')
        with open(path, 'rb') as f:
            form = {
                'file': f,
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

    def test_xls_importer_with_tag(self):
        path = join(dirname(__file__), 'test1.xls')
        tag_name = 'Test tag'
        with open(path, 'rb') as f:
            form = {
                'file': f,
                'tag_name': tag_name
            }

            response = self.client.post('/admin/importer/xls_importer/',
                                        data=form)

        # el archivo deberia procesarse correctamente
        self.assertEqual(response.status_code, 200)

        # deberia haber una tag
        self.assertEqual(Tag.objects.all().count(), 1)

        # todos los gastos creados deberian tener la etiqueta
        tags = [s.tags.first().name for s in Spending.objects.all()]
        self.assertEqual(len(tags), 9)
        tags = list(set(tags))
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0], tag_name)

