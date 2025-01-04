from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import TeacherLoginForm
from .models import Teacher


def TeacherLoginView(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            password = form.cleaned_data['password']

            # teacher_idを基に教師を認証
            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                if teacher.check_password(password):
                    login(request, teacher)  # teacherオブジェクトが認証に成功した場合ログイン
                    return redirect('students:index')  # 成功後のリダイレクト先
                else:
                    messages.error(request, 'パスワードが間違っています。')
            except Teacher.DoesNotExist:
                messages.error(request, '教師IDが間違っています。')

    else:
        form = TeacherLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

