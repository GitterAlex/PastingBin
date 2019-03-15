#views.py
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse, Http404
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
    #Prevent Admins or Staff from creating posts
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/HostessPasties/admin')
    #if users are authenticated, then they will be able to create a post
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
#dashboard page
def dashboard(request):
    #admins or staff have to use the admin portal
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/HostessPasties/admin')
    #create querysets for the selected users posts and public posts
    userposts = PostTable.objects.filter(owner=request.user.id)
    publicposts = PostTable.objects.filter(private=0)[:10]
    #send posts to html page if users are logged in
    if request.user.is_authenticated:
        user_posts_html = {'userposts': userposts, 'publicposts': publicposts}
        return render(request, 'webpages/dashboard.html', user_posts_html)
    else:
        #if not logged in redirect to frontpage
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
            #if request is not post
            form = AccountCreation()
            context = {'form': form}
            return render(request, 'webpages/createaccount.html', context)
#using generic views we can update the user
class UserUpdate(UpdateView):
    #fields neccesary for updating user
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'webpages/user_form.html'
    #once successful we redirect back to dashboard
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user
#using generic views we can delete the user
class UserDelete(DeleteView):
    #fields neccesary for updating user
    model = User
    template_name = 'webpages/user_confirm_delete.html'
    success_url = reverse_lazy('frontpage')

    def get_object(self):
        return self.request.user
#change password definition
def change_password(request):
    #user has to be logged in to change password
    if request.user.is_authenticated:
        if request.method == 'POST':
            #forward to form for password change
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                #update_session_auth_hash(request, user)
                messages.success(request, 'Password Change Successful')
                return redirect('/HostessPasties/')
            else:
                #when form is not valid
                messages.error(request, 'There was something wrong with changing the password. Please try again.')
                return redirect('changepassword')
        else:
            #if method is not post
            form = PasswordChangeForm(request.user)
            context = {'form': form}
            return render(request, 'webpages/change_password.html', context)
    else:
        #if user is not logged in, redirect to home
        return redirect('/HostessPasties/')
#generic view updateview allows updating of posts
class PostUpdate(UpdateView):
    model = PostTable
    form_class = PostCreation
    template_name = 'webpages/posttable_form.html'
    success_url = reverse_lazy('dashboard')
#generic view updateview allows deleting of posts
class PostDelete(DeleteView):
    model = PostTable
    template_name = 'webpages/posttable_confirm_delete.html'
    success_url = reverse_lazy('frontpage')
#generic view updateview allows for easy viewing of posts
class PostView(DetailView):
    model = PostTable
    context_object_name = 'post_list'
    pk_url_kwarg = 'pk'
    template_name = 'webpages/posttable_view.html'
    #shows posts that are created by the user, private for the user and posts that the user have been invited to
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PostTable.objects.filter(Q(owner=self.request.user.id) | Q(private=0) | Q(postshares=self.request.user.id))
        else:
            return PostTable.objects.filter(private=0)
#search function
def search(request):
    if request.method == 'GET':
        #get search term from user in html page and save as post_content
        post_content = request.GET.get('q')
        #save as queryset
        queryset = PostTable.objects.annotate(search=SearchVector('title','pasteContent')).filter(search=post_content)
        #save query to context and render to html
        context = {'post': queryset}
        return render(request, 'webpages/search.html', context)
    else:
        return render(request, 'webpages/search.html', {})
#download function
def download(request, postID):
    #get query set from posttable where postID = postid from html page
    filename = PostTable.objects.filter(postID = postID).values('title')[0]
    queryset = PostTable.objects.filter(postID = postID).values('pasteContent')[0]
    #change queryset to formatted string
    fname = filename.get('title')
    content = queryset.get('pasteContent')
    #send back to html file and let user download
    response = HttpResponse(content, content_type='text/html charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename= "{}.txt"'.format(fname)
    return response
#shares function
def shared(request):
    if request.user.is_authenticated:
        #filter shares by userid only if user is logged in
        sharedposts = PostTable.objects.filter(postshares=request.user.id)
        #send query to html
        context = {'sharedposts': sharedposts}
        return render(request, 'webpages/post_shares.html', context)
    else:
        return redirect('/HostessPasties/')
