from django import forms
from .models import Notice, GalleryImage, Syllabus, Result,StaffMember

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_college_wide', 'subdepartment']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['category', 'title', 'image', 'subdepartment']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['subdepartment', 'title', 'file']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['subdepartment', 'title', 'file']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['subdepartment', 'name', 'designation', 'image', 'bio']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }