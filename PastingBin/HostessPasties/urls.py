#urls.py
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .models import PostTable

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('createpost/', views.createpost),
    path('createaccount/', views.createaccount),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change_password/', views.change_password, name='changepassword')
]
urlpatterns += [
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('<pk>/postdelete/', views.PostDelete.as_view(), name='post_delete'),
    path('<pk>/postupdate/', views.PostUpdate.as_view(), name='post_update'),
    path('<pk>/', views.PostView.as_view(), name='post_view')
]
