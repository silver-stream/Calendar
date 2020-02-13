
from django.shortcuts import render

import datetime


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


from django.contrib.auth.decorators import login_required

def myform(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'myform.html', {'form': form})

@login_required
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

@login_required
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
    interval = 30

    dt = datetime.datetime.now()
    start_time = dt
    start_time = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time_delta = datetime.timedelta(hours=12)
    dtstart = datetime.datetime.combine(dt.date(), start_time.time())
    dtend = dtstart + end_time_delta
    time_delta=datetime.timedelta(minutes=15)
    print(start_time)
    print(end_time_delta)
    print(dtstart)
    print(dtend)
    print(time_delta)



    timeslots = []
    n = dtstart
    while n <= dtend:
        timeslots.append( {'id':n.strftime("%H:%M"), 'chemblid': 'test','prefName': 'A'})
        n += time_delta

    rows=[]
    #for rowkey in sorted(timeslots):
    #    for colkey in rowkey:
    #        print (colkey)

    headers = Category.objects.all()
    #headers = ['ID','Data','Code']

    rows = [{'id': 1, 'chemblid': 'bbbbbbbb','prefName': 'A'},
            {'id': 2, 'chemblid': 234, 'prefName': 'B'},
            {'id': 3, 'chemblid': 23454, 'prefName': 'C'},
            {'id': 4, 'chemblid': 6456, 'prefName': 'D'}]

    print(timeslots)

    return render(request, 'table.html', {'header': headers, 'rows': timeslots})


def day_view(request, year, month, day, template='daily_view.html', **params):
    '''
    See documentation for function``_datetime_view``.

    '''
    dt = datetime(int(year), int(month), int(day))
    return _datetime_view(request, template, dt, **params)
