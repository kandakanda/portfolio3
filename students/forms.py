from django import forms
from .models import Student
from django.db.models import fields


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('last_name','first_name','ent_year', 'class_id','postalcode','address1','address2','phone_number','attend_flag',)
        
    def __init__(self, *args, **kwargs):
        # `is_create` フラグを引数として受け取る
        is_create = kwargs.pop('is_create', False)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['last_name'].widget.attrs['placeholder'] = '例：長野'
        self.fields['first_name'].widget.attrs['placeholder'] = '例：太郎'
        self.fields['ent_year'].widget.attrs['placeholder'] = '例：2024'
        self.fields['postalcode'].widget.attrs['placeholder'] = '例：3800921'
        self.fields['address1'].widget.attrs['placeholder'] = '例：長野県長野市栗田123'
        self.fields['address2'].widget.attrs['placeholder'] = '例：メゾン102'
        self.fields['phone_number'].widget.attrs['placeholder'] = '例：09012345678'
        
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['ent_year'].required = True
        self.fields['class_id'].required = True
        self.fields['postalcode'].required = True
        self.fields['address1'].required = True
        self.fields['phone_number'].required = True

        # 新規作成の場合は `attend_flag` を変更不可に設定
        if is_create:
            self.fields['attend_flag'].widget.attrs['disabled'] = True