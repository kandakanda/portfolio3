from django import forms
from students.models import Course
from accounts.models import Teacher
# from django.db.models import fields

class ClassCreateForm(forms.ModelForm):
    teacher_id = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),  # Teacher テーブルからすべてのデータを取得
        label="担当教師",  # フィールドのラベルを設定
        empty_label="教師を選択してください",  # 未選択時に表示されるテキスト
        widget=forms.Select(attrs={'class': 'form-control'})  # プルダウンのスタイル設定
    )

    class Meta:
        model = Course
        fields = ('class_id', 'course_name', 'teacher_id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 残りのフィールドに CSS クラスや属性を付与
        for field_name in ['class_id', 'course_name']:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'
            field.required = True

        # プレースホルダを設定
        self.fields['class_id'].widget.attrs['placeholder'] = '例：101'
        self.fields['course_name'].widget.attrs['placeholder'] = '例：システム開発コース'
