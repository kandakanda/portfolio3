from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('top/', views.IndexView.as_view(), name='index'),
    path('student_list/', views.student_listView, name='stu_list'),
    path('student_create/', views.StudentCreateView.as_view(), name='stu_create'),
    path('student_detail/', views.StudentDetailView, name='stu_detail'),
    path('student_update/', views.StudentUpdateView, name='stu_update'),
    # path('student_update_execute/<str:pk>/', views.StudentUpdateExecuteView.as_view(), name='stu_update'),
    
]