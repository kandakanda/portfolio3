from django.contrib import admin
from django import forms
from .forms import TeacherForm
from .models import Teacher

# 管理画面で使用するTeacherAdminをカスタマイズ
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm  # カスタマイズしたフォームを使用
    list_display = ('teacher_id', 'teacher_name', 'class_id', 'is_active', 'is_staff')  # 一覧で表示するカラム
    list_filter = ('is_staff', 'is_active')  # 管理者がレコードを絞り込んで表示できる
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('teacher_id', 'password', 'is_staff', 'is_active')}
        ),
    )

    ordering = ('teacher_id',)


admin.site.register(Teacher, TeacherAdmin)
