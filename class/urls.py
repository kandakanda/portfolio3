from django.urls import path
from . import views

app_name = 'class'

urlpatterns = [
    path('cls_list/', views.ClassListView, name='cls_list'),
    path('cls_create/', views.ClassCreateView.as_view(), name='cls_create'),
    path('cls_update/<str:pk>/', views.ClassUpdateView.as_view(), name='cls_update'),
    path('cls_delete/<str:pk>/', views.ClassDeleteView.as_view(), name='cls_delete'),
    
]