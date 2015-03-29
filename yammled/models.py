# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.db.models.fields import (CharField, IntegerField, DateField)
import yaml
from datetime import date
from django.forms import ModelForm


def get_models(model_file):
    """
        load models from file to dict
    :param model_file:
    :return:
    """
    models = yaml.load(open(model_file))
    return models


def load_models(model_file):
    """
        get file and return models
    :param model_file:
    :return:
    """
    yaml_models = get_models(model_file)
    ready_models = []
    for model in yaml_models:
        model_name = model.capitalize()

        model_title = yaml_models[model]['title']
        model_options = {'verbose_name': model_title}
        yaml_fields = yaml_models[model]['fields']
        model_fields = {
            '__module__': __name__,
            'id': models.AutoField(primary_key=True)
        }
        for field in yaml_fields:
            if field['type'] == 'int':
                model_fields[field['id']] = \
                    IntegerField(verbose_name=field['title'], default=0)
            elif field['type'] == 'char':
                model_fields[field['id']] = \
                    CharField(max_length=255, verbose_name=field['title'],
                              default='')
            elif field['type'] == 'date':
                model_fields[field['id']] = \
                    DateField(verbose_name=field['title'], default=date.today())

        new_model = create_model(model_name,
                                         model_fields,
                                         options=model_options,
                                         app_label='yammled',
                                         admin_opts={})
        ready_models.append(new_model)
        globals()[model_name] = new_model

        # ModelForms is very similar to models creation. Do it directly
        form_name = "{0}Form".format(model_name)
        globals()[form_name] = type(form_name, (ModelForm,), {
            'Meta': type('Meta', (object,), {'model': new_model, 'fields': '__all__'})
        })

    return ready_models


def create_model(name, fields=None, app_label='', module='',
                 options=None, admin_opts=None):
    """
      Create specified model (from djangoproject wiki)
    """
    class Meta:
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model

from django.conf import settings
m_file = settings.YAML_PATH
tables = load_models(m_file)
models_data = get_models(m_file)