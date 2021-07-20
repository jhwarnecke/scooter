from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='editindex'),
    path('editfunc', views.editfunc, name='editfunc') 

]