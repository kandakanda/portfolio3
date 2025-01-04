from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from decimal import Decimal
from scores.models import Subject
from accounts.models import Teacher

class Course(models.Model):
    """クラスモデル
        クラス名を管理しているテーブル
    """
    class_id = models.CharField(verbose_name='クラス番号', max_length=3, primary_key=True)
    course_name = models.CharField(verbose_name='クラス名', max_length=20, blank=True, null=True)
    teacher_id = models.ForeignKey(Teacher, verbose_name='教師番号', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Course'
    
    def __str__(self):
        return self.class_id + self.course_name
    

# Create your models here.
class Student(models.Model):
    """学生モデル
        学生の個人情報を管理するテーブル
    """
    
    student_id = models.CharField(verbose_name='学生番号', max_length=10, primary_key=True)
    last_name = models.CharField(verbose_name='氏名', max_length=30, blank=True, null=True)
    first_name = models.CharField(verbose_name='名前', max_length=30, blank=True, null=True)

    postalcode_regex = RegexValidator(regex=r'\d{7}', message=("※ハイフンなしの半角数字で入力してください"))
    postalcode = models.CharField(verbose_name='郵便番号', validators=[postalcode_regex, MinLengthValidator(7)], default='', max_length=7)

    address1 = models.CharField(verbose_name='住所1', max_length=40, blank=True, null=True)
    address2 = models.CharField(verbose_name='住所2(アパート名など)', max_length=50, blank=True, null=True)

    phone_number_regex = RegexValidator(regex=r'0[789]0\d{4}\d{4}', message = ("※ハイフンなしの半角数字で入力してください"))
    phone_number = models.CharField(verbose_name='電話番号', validators=[phone_number_regex, MinLengthValidator(11)], blank=True, null=True)

    ent_year = models.IntegerField(verbose_name='入学年度', blank=True, null=True)
    class_id = models.ForeignKey(Course, verbose_name='クラス番号', on_delete=models.PROTECT)
    absence_day = models.DecimalField(verbose_name='欠席累計', default=Decimal('0.0'), max_digits=3, decimal_places=1)
    attend_flag = models.BooleanField(verbose_name='在籍フラグ', default=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Student'
    
    def __str__(self):
        return self.student_id + ',' + self.last_name + self.first_name
    

class Score(models.Model):
    """成績モデル
        学生の成績情報を管理するテーブル
    """
    student_id = models.ForeignKey(Student, verbose_name='学生番号', on_delete=models.PROTECT)
    subject_id = models.ForeignKey(Subject, verbose_name='科目番号', on_delete=models.PROTECT)
    score = models.IntegerField(verbose_name='点数', default=0)

    class Meta:
        verbose_name_plural = 'Score'
    
    def __str__(self):
        return f'{self.student_id.student_id} - {self.subject_id.subject_id}'