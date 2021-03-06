import logging
from django_pandas.io import read_frame

from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS, load_backend

import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd

import pandas as pd
from django.shortcuts import render

from datetime import datetime, timedelta, time

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import CreateView, TemplateView

from .models import Board, AverageWind
from .models import Category

from .models import Wind

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
    interval = 30

    dt = datetime.now()
    start_time = dt
    start_time = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time_delta = timedelta(hours=12)
    dtstart = datetime.combine(dt.date(), start_time.time())
    dtend = dtstart + end_time_delta
    time_delta = timedelta(minutes=15)
    print(start_time)
    print(end_time_delta)
    print(dtstart)
    print(dtend)
    print(time_delta)

    timeslots = []
    n = dtstart
    while n <= dtend:
        timeslots.append({'id': n.strftime("%H:%M"), 'chemblid': 'test', 'prefName': 'A', 'dt': n})
        n += time_delta

    rows = []
    # for rowkey in sorted(timeslots):
    #    for colkey in rowkey:
    #        print (colkey)

    headers = Category.objects.all()
    # headers = ['ID','Data','Code']

    rows = [{'id': 1, 'chemblid': 'bbbbbbbb', 'prefName': 'A'},
            {'id': 2, 'chemblid': 234, 'prefName': 'B'},
            {'id': 3, 'chemblid': 23454, 'prefName': 'C'},
            {'id': 4, 'chemblid': 6456, 'prefName': 'D'}]

    print(timeslots)

    return render(request, 'table.html', {'header': headers, 'rows': timeslots})


def day_view(request, year, month, day, template='day-view.html', **params):
    '''
    See documentation for function``_datetime_view``.

    '''
    dt = datetime(int(year), int(month), int(day))
    return render(request, 'day-view.html', {'dt': dt})


def add_event(
        request,
        template='add-event.html',
        #    event_form_class=forms.EventForm,
):
    '''
    Add a new ``Event`` instance and 1 or more associated ``Occurrence``s.

    Context parameters:

    ``dtstart``
        a datetime.datetime object representing the GET request value if present,
        otherwise None

    ``event_form``
        a form object for updating the event

    ``recurrence_form``
        a form object for adding occurrences

    '''
    dtstart = None
    if request.method == 'POST':
        x = 1
        # event_form = event_form_class(request.POST)
        # recurrence_form = recurrence_form_class(request.POST)
        # if event_form.is_valid() and recurrence_form.is_valid():
        #   event = event_form.save()
        #   recurrence_form.save(event)
        #   return http.HttpResponseRedirect(event.get_absolute_url())

    else:
        if 'dtstart' in request.GET:
            try:
                dtstart = datetime.strptime(request.GET['dtstart'], "%Y-%m-%dT%H:%M:%S")

            except(TypeError, ValueError) as exc:
                # TODO: A badly formatted date is passed to add_event
                logging.warning(exc)

        dtstart = dtstart or datetime.now()

        # event_form = event_form_class()
        # recurrence_form = recurrence_form_class(initial={'dtstart': dtstart})

    return render(
        request,
        template,
        {'dtstart': dtstart}
    )


def graph(request):

    wf = Wind.objects.all()

    avgWind = AverageWind.objects.all()
    print(avgWind.query)
    aw = int(0)

    for x in avgWind:
        aw= x.average_wind
    print (aw);

    df = read_frame(wf)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.created_at, y=df['wind_speed'], name="Wind Speed",
                             line_color='deepskyblue'))

    fig.add_trace(go.Scatter(x=df.created_at, y=df['highest_gust'], name="Gust Speed",
                             line_color='dimgray'))

    fig.update_layout(title_text='Wind Speed',
                      xaxis_rangeslider_visible=True)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=1000)

    div = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, 'graph.html', {'graph': div, 'average': aw})
