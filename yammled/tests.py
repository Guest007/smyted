# -*- coding: utf-8 -*-
from datetime import date
import random
import string
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
            # print instance.__dict__
            self.assertIsNotNone(id, msg="can't save %s" % instance.__repr__())
            self.assertEqual(Model.objects.get(id=id),
                             instance,
                             msg=" can't get %s" % instance.__repr__())
