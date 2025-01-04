from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class TeacherManager(BaseUserManager):
    """カスタムユーザーマネージャー"""

    def create_user(self, teacher_id, password=None, is_staff=False, **extra_fields):
        """
        ユーザーを作成する際に is_staff フラグを設定できる。
        管理画面用に作成。
        """
        if not teacher_id:
            raise ValueError('教師IDは必須です。')
        extra_fields.setdefault('is_active', True)  # デフォルトでアクティブ
        extra_fields['is_staff'] = is_staff  # is_staff フラグを設定可能
        user = self.model(teacher_id=teacher_id, **extra_fields)
        user.set_password(password)  # パスワードをハッシュ化
        user.save(using=self._db)
        return user

    def create_superuser(self, teacher_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(teacher_id, password, **extra_fields)

# Create your models here.
class Teacher(AbstractBaseUser, PermissionsMixin):
    """教師モデル
        教師の情報を管理するテーブル
    """
    teacher_id = models.IntegerField(verbose_name='教師番号', primary_key=True)
    teacher_name = models.CharField(verbose_name='教師名', max_length=30, blank=True, null=True)
    password = models.CharField(verbose_name='パスワード', max_length=256, blank=True, null=True)
    class_id = models.CharField(verbose_name='クラス番号', max_length=3, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # 退職フラグ
    is_staff = models.BooleanField(default=False)  # 管理者フラグ

    objects = TeacherManager()

    USERNAME_FIELD = 'teacher_id'  # ログインに使用するフィールド
    REQUIRED_FIELDS = []  # 必須項目

    class Meta:
        verbose_name_plural = 'Teacher'

    def set_password(self, password):
        """パスワードをハッシュ化して保存するメソッド"""
        self.password = make_password(password)
        
    def check_password(self, password):
        """パスワードのチェック"""
        return check_password(password, self.password)
    
    def __str__(self):
        return f"{self.teacher_id} ({self.teacher_name})"