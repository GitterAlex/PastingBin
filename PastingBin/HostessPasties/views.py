#views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .admin import AccountCreationForm

#frontpage rendering
def frontpage(request):
    return render(request,'webpages/frontpage.html')
#Create post function
def createpost(request):
    return render(request, 'webpages/createpost.html')
def dashboard(request):
    return render(request, 'webpages/dashboard.html')
#create account defnition
def createaccount(request):
    #the request must be a POST
    if request.user.is_authenticated:
        return redirect('/HostessPasties/dashboard')
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
                context = {'form': form
                }
                return render(request, 'webpages/createaccount.html', context)
        else:
            form = AccountCreationForm()
            context = {'form': form
            }
            return render(request, 'webpages/createaccount.html', context)
