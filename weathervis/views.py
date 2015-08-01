from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def index(request):
	return render_to_response('weathervis/weathervis.html')