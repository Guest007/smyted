# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core import serializers
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
import json
import sys
import models


def obj_create(request, mod_id=None):
    """
        Create new model's object
    """
    if mod_id:
        form_name_name = "{0}Form".format(mod_id.capitalize())
    else:
        raise Http404

    # check model's form class is exist
    if request.POST and hasattr(models, form_name_name):
        form_name = getattr(models, form_name_name)
        form = form_name(request.POST)
        obj = form.save()
        return HttpResponse(json.dumps(obj.id),
                            content_type="application/json")
    else:
        raise Http404


def obj_update(request, mod_id=None):
    """
        Update model's field through POST
    """
    if mod_id:
        model = mod_id.capitalize()
    else:
        raise Http404

    if request.POST and hasattr(models, model):
        try:
            obj_cls = getattr(models, model)
            pk = request.POST['objid']
            field = request.POST['field']
            value = request.POST['value']
            obj = get_object_or_404(obj_cls, id=pk)
            setattr(obj, field, value)
            obj.save()
            return HttpResponse(json.dumps('ok'),
                                content_type="application/json")
        except:
            raise Http404
    else:
        raise Http404


def json_obj(request, mod_id=None):
    """
        Get list of objects in JSON
    """
    if mod_id:
        model = mod_id.capitalize()
    else:
        raise Http404
    if hasattr(models, model):
        form_name = getattr(models, "{0}Form".format(model))
        obj_name = getattr(models, model)
    else:
        raise Http404
    return HttpResponse(serializers.serialize('json',
                                              obj_name.objects.all()),
                        content_type="application/json")


def get_models_in_json(request):
    """
        Get model's config in JSON
    """
    return HttpResponse(json.dumps(models.models_data),
        content_type="application/json")


def homepage(request):
    """
        Homepage with moels list
    """
    return render_to_response('yammled/homepage.html',
                              {'maxint': sys.maxint},
                              context_instance=RequestContext(request))

