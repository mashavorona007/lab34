from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

class IndexPage(TemplateView): 
    template_name = 'index.html'
    