from django.db import models

# Create your models here.
class Subject(models.Model):
    """科目モデル
        科目情報を管理するテーブル
    """
    
    subject_id = models.CharField(verbose_name='科目番号', max_length=10, primary_key=True)
    subject_name = models.CharField(verbose_name='科目名', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Subject'
    
    def __str__(self):
        return self.subject_id + ',' + self.subject_name
    