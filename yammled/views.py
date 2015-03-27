# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
import models


class Home(TemplateView):
    template_name = 'yammled/homepage.html'

    def get_context_data(self, **kwargs):
        """
            Prepare data for displaying
            (left menu)

        :param kwargs:
        :return:
        """
        context = super(Home, self).get_context_data(**kwargs)

        models_names = []
        for i in models.tables:
            models_names.append({'name': i._meta.original_attrs['verbose_name'],
                                 'model': i._meta.object_name
                                 }
            )


        context['models'] = models_names
        # print context

        return context

