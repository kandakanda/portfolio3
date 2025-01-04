from django.db import models
from students.models import Student
# Create your models here.
class Attendance(models.Model):
    """出欠席モデル
        クラス名を管理しているテーブル
    """
    student_id = models.ForeignKey(Student, verbose_name='学生番号', on_delete=models.PROTECT)
    attendance_date = models.DateField(verbose_name='遅刻・早退・欠席日', blank=True, null=True)
    attendance_id = models.IntegerField(verbose_name='分類(1:欠席, 2: 遅刻, 3:早退, 4:その他)', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Attendance'
    
    def __str__(self):
        return f'{self.student_id.student_id} - {self.attendance_date}'