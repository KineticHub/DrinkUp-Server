#DrinkUp/ApiApp

import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.db.models import Q

from MainApp.models import *

def Bars(request, zipcode):

    if request.method == 'GET':
        pass
