from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('at_search/', views.AttendanceSearchView, name='at_search'),
    path('at_insert/', views.AttendanceInsertView, name='at_insert'),
    
]