# -*- coding: utf-8 -*-
from datetime import date
import random
import string
from django.shortcuts import get_object_or_404
from django.test import TestCase
import models


class ModelsTest(TestCase):

    def setUp(self):
        self.models = []
        for i in models.tables:
            self.models.append(i)

    def test_save_and_get(self):

        initials = ['', 0]
        for Model in self.models:
            instance = Model()
            # print instance.__dict__

            for fieldname in instance.__dict__:
                if fieldname[0] == '_':
                    continue
                if fieldname == 'id':
                    continue
                field = getattr(instance, fieldname)
                if isinstance(field, unicode):
                    setattr(instance, fieldname,
                            u''.join([random.choice(string.letters)
                                      for i in xrange(20)]))
                elif isinstance(field, int):
                    setattr(instance, fieldname, random.randrange(100000))
                elif isinstance(field, date):
                    setattr(instance, fieldname,
                            date(random.randrange(1950, 2020),
                                 random.randrange(1, 12),
                                 random.randrange(1, 28)))

                self.assertNotIn(getattr(instance, fieldname), initials)

            instance.save()
            id = instance.id
            self.assertIsNotNone(id, msg="can't save %s" % instance.__repr__())
            self.assertEqual(Model.objects.get(id=id),
                             instance,
                             msg=" can't get %s" % instance.__repr__())


class ViewsTestsCase(TestCase):

    def setUp(self):
        self.field_values = {
            'char': ''.join([random.choice(string.letters) for i in xrange(20)]),
            'int': random.randrange(100000),
            'date': date.today()
        }
        self.doc = models.models_data

    def test_index_get(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_json_cls_get(self):
        resp = self.client.get('/json_cls/')
        self.assertEqual(resp.status_code, 200)

    def test_json_obj_get(self):
        for model_id in self.doc.keys():
            resp = self.client.get('/json_obj/{0}/'.format(model_id))
            self.assertEqual(resp.status_code, 200)

    def test_obj_create_post(self):
        for model_id in self.doc.keys():
            params = {}
            for field in self.doc[model_id]['fields']:
                params[field['id']] = self.field_values[field['type']]
            resp = self.client.post('/obj_create/{0}/'.format(model_id), params)
            self.assertEqual(resp.status_code, 200)

    def test_obj_update_post(self):
        new_field_val = {
            'char': ''.join([random.choice(string.letters) for i in xrange(20)]),
            'int': random.randrange(100000),
            'date': date.today().strftime('%Y-%m-%d')
        }
        for model_id in self.doc.keys():
            model_cls_name = model_id.capitalize()
            model_cls = getattr(models, model_cls_name)
            kw = {}
            for field in self.doc[model_id]['fields']:
                kw[field['id']] = self.field_values[field['type']]
            model_obj = model_cls(**kw)
            model_obj.save()

            for field in self.doc[model_id]['fields']:
                params = {
                    'objid': model_obj.id,
                    'field': field['id'],
                    'value': new_field_val[field['type']]
                }
                resp = self.client.post('/obj_update/{0}/'.format(model_id), params)
                self.assertEqual(resp.status_code, 200)
                model_obj = get_object_or_404(model_cls, id=model_obj.id)
                field_val = getattr(model_obj, field['id'])
                if field['type'] == 'date':
                    field_val = field_val.strftime('%Y-%m-%d')
                self.assertEqual(field_val, new_field_val[field['type']])



