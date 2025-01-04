from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.contrib import messages

app_name = 'accounts'

class TeacherLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.info(request, 'ログアウトしました。')
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('login/', views.TeacherLoginView, name='login'),
    path('logout/', TeacherLogoutView.as_view(), name='logout'),    
]
