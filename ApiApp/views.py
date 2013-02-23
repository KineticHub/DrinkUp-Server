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

def AllBars(request):

    if request.method == 'GET':
        
        bars_to_return = Bar.objects.all()
        
        json_serializer = serializers.get_serializer("json")()
	response = json_serializer.serialize(bars_to_return, ensure_ascii=False)
	return HttpResponse(response, mimetype="application/json")
        
