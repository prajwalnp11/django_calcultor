from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def root(request):
    return HttpResponse("server started")
