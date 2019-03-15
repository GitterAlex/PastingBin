#urls.py
from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .models import PostTable

urlpatterns = [
    #home page
    path('', views.frontpage, name='frontpage'),
    #admin login page
    path('admin/', admin.site.urls),
    #create post page
    path('createpost/', views.createpost),
    #create account page
    path('createaccount/', views.createaccount),
    #home page for users who are logged in
    path('dashboard/', views.dashboard, name='dashboard'),
    #change password for users
    path('change_password/', views.change_password, name='changepassword'),
    #search results page
    path('search/', views.search, name='search'),
    #download page uses postID as a parameter
    re_path(r'(?P<postID>[\w\-]+)/download$', views.download, name='download'),
    #Share page
    path('shared/', views.shared, name='shared')
]
#URLs for generic views
urlpatterns += [
    #update user page as view
    url(r'^update/', views.UserUpdate.as_view(), name='user_update'),
    #delete user page as view
    url(r'^delete/', views.UserDelete.as_view(), name='user_delete'),
    #delte post page as view with the primary key in the url
    path('<pk>/postdelete/', views.PostDelete.as_view(), name='post_delete'),
    #update post page as view with the primary key in the url
    path('<pk>/postupdate/', views.PostUpdate.as_view(), name='post_update'),
    #view post page as view with the primary key in the url
    path('<pk>/', views.PostView.as_view(), name='post_view')
]
