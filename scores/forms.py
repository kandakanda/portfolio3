from django import forms
from .models import Subject
from django.db.models import fields


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('subject_id','subject_name',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['subject_id'].widget.attrs['placeholder'] = '例：A01'
        self.fields['subject_name'].widget.attrs['placeholder'] = '例：数学'
        
        self.fields['subject_id'].required = True
        self.fields['subject_name'].required = True
