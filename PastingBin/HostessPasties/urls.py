#urls.py
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

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
<<<<<<< HEAD
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete')
=======
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('<pk>/postupdate/', views.PostUpdate.as_view(), name='post_update'),
>>>>>>> b2a0e5b8df68d8a12b73fe93fff9ff45345b4003
]
