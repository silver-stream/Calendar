from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import CreateView, TemplateView

from .models import Board
from .models import Category

import urllib
import json

from django.shortcuts import render
from .forms import DictionaryForm, FindMyShiftForm


from django.shortcuts import render
from .forms import ContactForm

def myform(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'myform.html', {'form': form})


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def oxford(request):
    search_result = {}
    if 'word' in request.GET:
        form = DictionaryForm(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = DictionaryForm()
    return render(request, 'oxford.html', {'form': form, 'search_result': search_result})


def shift(request):
    search_result = {}
    if 'word' in request.GET:
        form = FindMyShiftForm(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = FindMyShiftForm()
    return render(request, 'shift.html', {'form': form, 'search_result': search_result})

def table(request):

    headers = Category.objects.all()
    #headers = ['ID','Data','Code']
    rows = [{'id': 1, 'chemblid': 'bbbbbbbb','prefName': 'A'},
            {'id': 2, 'chemblid': 234, 'prefName': 'B'},
            {'id': 3, 'chemblid': 23454, 'prefName': 'C'},
            {'id': 4, 'chemblid': 6456, 'prefName': 'D'}]

    return render(request, 'table.html', {'header': headers, 'rows': rows})
