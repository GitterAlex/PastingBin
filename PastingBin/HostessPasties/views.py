#views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AccountCreation
from .forms import PostCreation
from .models import PostTable
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django import forms
from django.db.models import Q

#frontpage rendering
def frontpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')
    else:
        return render(request,'webpages/frontpage.html')
#Create post function
def createpost(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/HostessPasties/admin')
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
                return redirect('/HostessPasties/dashboard/')
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

def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/HostessPasties/admin')

    userposts = PostTable.objects.filter(owner=request.user.id)
    publicposts = PostTable.objects.filter(private=0)[:10]
    if request.user.is_authenticated:
        user_posts_html = {'userposts': userposts, 'publicposts': publicposts}
        return render(request, 'webpages/dashboard.html', user_posts_html)
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
            form = AccountCreation(request.POST)
            #If all inputs are valid save to the database and redirect to home page
            if form.is_valid():
                form.save()
                return redirect('/HostessPasties')
                #if not reload the create account page
            else:
                context = {'form': form}
                return render(request, 'webpages/createaccount.html', context)
        else:
            form = AccountCreation()
            context = {'form': form}
            return render(request, 'webpages/createaccount.html', context)

class UserUpdate(UpdateView):
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name']
    template_name = 'webpages/user_form.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

class UserDelete(DeleteView):
    model = User
    template_name = 'webpages/user_confirm_delete.html'
    success_url = reverse_lazy('frontpage')

    def get_object(self):
        return self.request.user

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                #update_session_auth_hash(request, user)
                messages.success(request, 'Password Change Successful')
                return redirect('/HostessPasties/')
            else:
                messages.error(request, 'There was something wrong with changing the password. Please try again.')
                return redirect('changepassword')
        else:
            form = PasswordChangeForm(request.user)
            context = {'form': form}
            return render(request, 'webpages/change_password.html', context)
    else:
        return redirect('/HostessPasties/')
class PostUpdate(UpdateView):
    model = PostTable
    form_class = PostCreation
    template_name = 'webpages/posttable_form.html'
    success_url = reverse_lazy('dashboard')

class PostDelete(DeleteView):
    model = PostTable
    template_name = 'webpages/posttable_confirm_delete.html'
    success_url = reverse_lazy('frontpage')

class PostView(DetailView):
    model = PostTable
    context_object_name = 'post_list'
    pk_url_kwarg = 'pk'
    template_name = 'webpages/posttable_view.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PostTable.objects.filter(Q(owner=self.request.user.id) | Q(private=0))
        else:
            return PostTable.objects.filter(private=0)

def search(request):
    if request.method == 'GET':
        post_content = request.GET.get('q')
        queryset = PostTable.objects.annotate(search=SearchVector('title','pasteContent')).filter(search=post_content)
    #    user = User.objects.annotate(search=SearchVector('id')).filter(search=queryset)
        context = {'post': queryset}
        return render(request, 'webpages/search.html', context)
    else:
        return render(request, 'webpages/search.html', {})
