# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView


class Home(ListView):
    template_name = 'yammled/homepage.html'

