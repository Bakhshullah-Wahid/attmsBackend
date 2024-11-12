# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

urlpatterns = [
    path('departments/', views.DepartmentView.as_view()),
     path('departments/delete/<int:pk>/', views.DepartmentView.as_view(), name='delete-department'),
     path('departments/update/<int:pk>/',views.DepartmentView.as_view() , name='update-department'),
    #  classs path setting
    path('classs/',views.ClasssView.as_view()),
    path('classs/delete/<int:pk>/' , views.ClasssView.as_view() , name='delete-classs'),
    path('classs/update/<int:pk>/' , views.ClasssView.as_view() , name='update-classs') ,
    #user path coordinator
    path('users/', views.UserView.as_view()),
     path('users/update/<int:pk>/' , views.UserView.as_view() , name='update-users') ,
     path('users/delete/<int:pk>/' , views.UserView.as_view() , name='delete-users'),

     #teacher path setting

     path('teachers/',views.TeacherView.as_view()),
     path('teachers/update/<int:pk>/' , views.TeacherView.as_view() , name='update-teachers') ,
       path('teachers/delete/<int:pk>/' , views.TeacherView.as_view() , name='delete-teacher'),

       #email verification
       path('verify-email/', views.verify_email, name='verify_email'),
       path('initiate-email-verification/', views.initiate_email_verification, name='initiate_email_verification'),
]
