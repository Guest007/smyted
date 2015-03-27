# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.db.models.fields import (CharField, IntegerField, DateField)
import yaml
from datetime import date


def load_models(model_file):
    yaml_models = yaml.load(open(model_file))
    ready_models = []
    for model in yaml_models:
        model_name = model
        model_title = yaml_models[model]['title']
        model_options = {'verbose_name': model_title}
        yaml_fields = yaml_models[model]['fields']
        model_fields = {}
        for field in yaml_fields:
            if field['type'] == 'int':
                model_fields[field['id']] = \
                    IntegerField(verbose_name=field['title'], default=0)
            elif field['type'] == 'char':
                model_fields[field['id']] = \
                    CharField(max_length=255, verbose_name=field['title'], default='')
            elif field['type'] == 'date':
                model_fields[field['id']] = \
                    DateField(verbose_name=field['title'], default=date.today())

        ready_models.append(create_model(model_name,
                                         model_fields,
                                         options=model_options,
                                         app_label='yammled',
                                         admin_opts={})
                            )
    return ready_models


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
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

