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
        fields = ['sub_department', 'title', 'file', 'pdf_upload']
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



from django import forms
from .models import StaffMember


class ListFormField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

    def prepare_value(self, value):
        if value is None:
            return ''
        return ', '.join(value)

class StaffMemberForm(forms.ModelForm):
    qualifications_normal = ListFormField(label='Qualifications')
    mobile_numbers_normal = ListFormField(label='Mobile Numbers')
    email_addresses_normal = ListFormField(label='Email Addresses')
    research_co_supervision_normal = ListFormField(label='Research Co-Supervision')
    awards_and_recognition_normal = ListFormField(label='Awards & Recognition')
    professional_activities_normal = ListFormField(label='Professional Activities')

    class Meta:
        model = StaffMember
        fields = [
            'sub_department',
            'department',
            'name',
            'designation',
            'photo',
            'email',
            'phone',
            'specialization',
            'career_summary',
            'qualifications_normal',
            'mobile_numbers_normal',
            'email_addresses_normal',
            'research_co_supervision_normal',
            'awards_and_recognition_normal',
            'research_publications',
            'professional_activities_normal',
            'work_experience',
        ]
        widgets = {
            'qualifications': forms.HiddenInput(),
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'department': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'patents': forms.Textarea(attrs={'class': 'form-control'}),
            'research_publications': forms.Textarea(attrs={'class': 'form-control'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['qualifications'] = cleaned_data.get('qualifications_normal', [])
        # If qualifications_normal is a list, join it. If it's already a string, use it.
        if isinstance(cleaned_data['qualifications'], list):
            cleaned_data['qualifications'] = ', '.join(cleaned_data['qualifications'])
        return cleaned_data



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_college_wide', 'sub_department', 'pdf_upload']
        widgets = {
            'sub_department': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }
