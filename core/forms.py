from django import forms
from .models import GalleryImage, Syllabus, Result, StaffMember, Notice, SubDepartment, GalleryCategory

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['category', 'title', 'image', 'sub_department']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['sub_department', 'title', 'file']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['sub_department', 'title', 'file']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['sub_department', 'name', 'designation', 'photo', 'email', 'phone']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_college_wide', 'sub_department']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }
