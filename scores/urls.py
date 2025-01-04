from django.urls import path
from . import views

app_name = 'scores'

urlpatterns = [
    path('scorelist/', views.ScorelistView, name='score_list'),
    path('scoreexecute/', views.ScoreExecuteView, name='score_execute'),
    path('sublist/', views.SubjectListView, name='sub_list'),
    path('subcreate/', views.SubjectCreateView.as_view(), name='sub_create'),
    path('subupdate/<str:pk>/', views.SubjectUpdateView, name='sub_update'),
    path('subdelete/<str:pk>/', views.SubjectDeleteView.as_view(), name='sub_delete'),
    
]