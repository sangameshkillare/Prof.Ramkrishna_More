from django.contrib import admin
from .models import Department, SubDepartment, Notice, GalleryCategory, GalleryImage, Syllabus, Result, DepartmentAdminAccess, StaffMember
from django.contrib.auth.models import User
from django import forms

class SubDepartmentInline(admin.TabularInline):
    model = SubDepartment
    extra = 1

class DepartmentAdminForm(forms.ModelForm):
    assigned_user_password = forms.CharField(widget=forms.PasswordInput(), label="Assigned User Password", required=False)

    class Meta:
        model = Department
        fields = ['name', 'user', 'assigned_user_password']

    def save(self, commit=True):
        department = super().save(commit=False)
        password = self.cleaned_data.get('assigned_user_password')
        user = self.cleaned_data.get('user')
        if user and password:
            user.set_password(password)
            user.save()
        if commit:
            department.save()
        return department

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    inlines = [SubDepartmentInline]
    form = DepartmentAdminForm

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'is_college_wide', 'department', 'subdepartment']
    list_filter = ['is_college_wide', 'department', 'subdepartment']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'is_college_wide', 'department', 'subdepartment']

class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category']
    search_fields = ['title']

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'department', 'subdepartment']
    list_filter = ['department', 'subdepartment']
    search_fields = ['title']

class ResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'department', 'subdepartment']
    list_filter = ['department', 'subdepartment']
    search_fields = ['title']

class DepartmentAdminAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'can_manage_notices', 'can_manage_gallery', 'can_manage_syllabus', 'can_manage_results', 'can_manage_staff']
    list_filter = ['department']
    search_fields = ['user__username', 'department__name']

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'subdepartment']
    list_filter = ['department', 'subdepartment']
    search_fields = ['name', 'designation']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(SubDepartment)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(GalleryCategory, GalleryCategoryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(DepartmentAdminAccess, DepartmentAdminAccessAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)




#password
#$Sang145766