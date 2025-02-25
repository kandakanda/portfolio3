# Generated by Django 4.2.17 on 2025-01-03 06:42

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('class_id', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='クラス番号')),
                ('course_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='クラス名')),
                ('teacher_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='教師番号')),
            ],
            options={
                'verbose_name_plural': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='学生番号')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='氏名')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='名前')),
                ('postalcode', models.CharField(default='', max_length=7, validators=[django.core.validators.RegexValidator(message='※ハイフンなしの半角数字で入力してください', regex='\\d{7}'), django.core.validators.MinLengthValidator(7)], verbose_name='郵便番号')),
                ('address1', models.CharField(blank=True, max_length=40, null=True, verbose_name='住所1')),
                ('address2', models.CharField(blank=True, max_length=50, null=True, verbose_name='住所2(アパート名など)')),
                ('phone_number', models.CharField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='※ハイフンなしの半角数字で入力してください', regex='0[789]0\\d{4}\\d{4}'), django.core.validators.MinLengthValidator(11)], verbose_name='電話番号')),
                ('ent_year', models.IntegerField(blank=True, null=True, verbose_name='入学年度')),
                ('absence_day', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=3, verbose_name='欠席累計')),
                ('attend_flag', models.BooleanField(blank=True, default=True, null=True, verbose_name='在籍フラグ')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.course', verbose_name='クラス番号')),
            ],
            options={
                'verbose_name_plural': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='点数')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.student', verbose_name='学生番号')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scores.subject', verbose_name='科目番号')),
            ],
            options={
                'verbose_name_plural': 'Score',
            },
        ),
    ]
