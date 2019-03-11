
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .admin import AccountCreationForm

def frontpage(request):
    return render(request,'webpages/frontpage.html')

def createpost(request):
    return render(request, 'webpages/createpost.html')

def createaccount(request):
    if request.method =='POST' :
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/HostessPasties')
        else:
            context = {'form': form
            }
            return render(request, 'webpages/createaccount.html', context)
    else:
        form = AccountCreationForm()
        context = {'form': form
        }
        return render(request, 'webpages/createaccount.html', context)
