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
    path('users/<int:department_id>/',views.UserView.as_view()),
     path('users/update/<int:pk>/' , views.UserView.as_view() , name='update-users') ,
     path('users/delete/<int:pk>/' , views.UserView.as_view() , name='delete-users'),

     #teacher path setting

     path('teachers/',views.TeacherView.as_view()),
     path('teachers/update/<int:pk>/' , views.TeacherView.as_view() , name='update-teachers') ,
       path('teachers/delete/<int:pk>/' , views.TeacherView.as_view() , name='delete-teacher'),
 #subjects path setup
    
     path('subjects/',views.SubjectView.as_view()),
     path('subjects/update/<int:pk>/' , views.SubjectView.as_view() , name='update-subjects') ,
       path('subjects/delete/<int:pk>/' , views.SubjectView.as_view() , name='delete-subjects'),
       #email verification
       path('send-email/', views.SendEmailView.as_view(), name='send_email'),
       #freeClass Slots
       path('free-class/',views.FreeClassView.as_view()),
       path('class/delete/<int:class_id>/<str:free_slots>/<str:day_of_week>/', views.FreeClassView.as_view(), name='delete_slot'),
      #  testing if it works
       path('class/<int:class_id>/',views.ClassDetailView.as_view(), name='class-detail'),
    path('scheduler/',views.SchedulerView.as_view()),
    path('scheduler/<int:department_id>/', views.SchedulerView.as_view(), name='scheduler-by-department'),

     
# -------------------------------------------------------------------------------------------------
   ]
