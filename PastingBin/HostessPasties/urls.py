#urls.py
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('createpost', views.createpost),
    path('createaccount', views.createaccount),
    path('dashboard', views.dashboard)

]
