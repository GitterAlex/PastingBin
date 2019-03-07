
from django.shortcuts import render
from django.http import HttpResponse

def frontpage(request):
    return render(request,'webpages/frontpage.html')

def createpost(request):
    return render(request, 'webpages/createpost.html')

def createaccount(request):
    return render(request, 'webpages/createaccount.html')
