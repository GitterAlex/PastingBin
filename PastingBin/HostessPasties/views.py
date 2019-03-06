
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'webpages/index.html')

def createpost(request):
    return render(request, 'webpages/createpost.html')
