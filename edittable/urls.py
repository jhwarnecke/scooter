from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='editindex'),
    path('editfunc', views.editfunc, name='editfunc'),  
    path('addfunc', views.addfunc, name='addfunc'),
    path('addfuncstart', views.addfuncstart, name='addfuncstart'),
    path('deletefuncstart', views.deletefuncstart, name='deletefuncstart'),
    path('deletefunc', views.deletefunc, name='deletefunc')




]