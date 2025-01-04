from django import forms
from .models import Teacher
from django.contrib.auth.forms import AuthenticationForm

# 管理画面で使用するフォームをカスタマイズ
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'teacher_name', 'password', 'class_id', 'is_active', 'is_staff',]

    def save(self, commit=True):
        # パスワードをハッシュ化
        teacher = super().save(commit=False)
        if teacher.password:
            teacher.set_password(teacher.password)
        if commit:
            teacher.save()
        return teacher

class TeacherLoginForm(forms.Form):
    teacher_id = forms.CharField(max_length=10, label="教師ID")
    password = forms.CharField(widget=forms.PasswordInput, label="パスワード")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
