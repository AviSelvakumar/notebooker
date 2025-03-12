from django.http import HttpResponse
from django.shortcuts import render
from eventStats import *

def questionList(request):

    return HttpResponse(getQuestionsJSON())

def interview(request):
    return render(request, 'interview.html')