from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


def index(request):
    return HttpResponse()