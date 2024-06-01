from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allEmp/', views.allEmp, name='allemps'),
    path('addEmp/', views.addEmp, name='addEmp'),
    path('findEmp/', views.findEmp, name='find'),
    path('rmEmp/', views.rmEmp, name='rm'),
    path('atd/', views.atdEmp, name='atd'),
    path('updEmp/<str:id>/', views.updEmp, name='upEmp'),
    path('delEmp/<str:id>/', views.delEmp, name='delEmp'),
    path('dataUpEmp/', views.dataUpEmp, name='dataUp'),
    path('mark_attendance/<str:id>/<int:status>', views.mark_attendance, name='mark_attendance'),
]