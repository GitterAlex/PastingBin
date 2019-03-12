#views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .admin import AccountCreationForm
from .forms import PostCreation
from .models import PostTable
#frontpage rendering
def frontpage(request):
    if request.user.is_authenticated:
        return render(request, 'webpages/dashboard.html')
    else:
        return render(request,'webpages/frontpage.html')
#Create post function
def createpost(request):
    if request.user.is_authenticated:
        if request.method =='POST' :
            #references the account creation form to give inputs
            form2 = PostCreation(request.POST)
            #If all inputs are valid save to the database and redirect to home page
            if form2.is_valid():
                post = form2.save(commit=False)
                post.owner = request.user
                form2.save()
                context = {'form2': form2}
                return render(request, 'webpages/dashboard.html', context)
                #if not reload the create account page
            else:
                context = {'form2': form2}
                return render(request, 'webpages/createaccount.html', context)
        else:
            form2 = PostCreation(request.POST)
            context = {'form2': form2}
            return render(request, 'webpages/createpost.html', context)
    else:
        return redirect('/HostessPasties')

def getPosts(request):
        fetchPForm = PostTable.objects.filter(owner=request.user.id)
        return render(request, 'webpages/dashboard.html', {'fetchPForm': fetchPForm})




def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'webpages/dashboard.html')
    else:
        return redirect('/HostessPasties/')
#create account defnition
def createaccount(request):
    #the request must be a POST
    if request.user.is_authenticated:
        return dashboard(request)
    else:
        if request.method =='POST' :
            #references the account creation form to give inputs
            form = AccountCreationForm(request.POST)
            #If all inputs are valid save to the database and redirect to home page
            if form.is_valid():
                form.save()
                return redirect('/HostessPasties')
                #if not reload the create account page
            else:
                context = {'form': form}
                return render(request, 'webpages/createaccount.html', context)
        else:
            form = AccountCreationForm()
            context = {'form': form}
            return render(request, 'webpages/createaccount.html', context)
