from django.contrib import admin
from .models import (
     Department,
     SubDepartment,
     SiteSettings,
     Notice,
     GalleryCategory,
     GalleryImage,
     Syllabus,
     Result,
     DepartmentAdminAccess,
     StaffMember,
     AboutUs,
     Event,
 )
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
 

class SubDepartmentInline(admin.TabularInline):
     model = SubDepartment
     extra = 1
 

class AboutUsInline(admin.StackedInline):
     model = AboutUs
     extra = 1
 

class SyllabusInline(admin.TabularInline):
     model = Syllabus
     extra = 1
 

class ResultInline(admin.TabularInline):
     model = Result
     extra = 1
 

class StaffMemberInline(admin.TabularInline):
     model = StaffMember
     extra = 1
 

class GalleryImageInline(admin.TabularInline):
     model = GalleryImage
     extra = 1
 

class NoticeInline(admin.TabularInline):
     model = Notice
     extra = 1
 

class EventInline(admin.TabularInline):
     model = Event
     extra = 1
 

class DepartmentAdminForm(forms.ModelForm):
     admin_access_user = forms.ModelChoiceField(
         queryset=User.objects.all(),
         label="Department Admin User",
     )
 

     class Meta:
         model = Department
         fields = "__all__"
 

     def save(self, commit=True):
         department = super().save(commit=commit)
         if commit:
             admin_user = self.cleaned_data["admin_access_user"]
             access, created = DepartmentAdminAccess.objects.get_or_create(
                 department=department, defaults={"user": admin_user}
             )
             if not created:
                 access.user = admin_user
                 access.save()
         return department
 

 

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
     inlines = [SubDepartmentInline]
     form = DepartmentAdminForm
     list_display = ("name", "slug")
     prepopulated_fields = {"slug": ("name",)}
     fields = ["name", "slug", "image", "description", "admin_access_user"]
 

 

@admin.register(SubDepartment)
class SubDepartmentAdmin(admin.ModelAdmin):
     list_display = ("name", "slug", "department")
     list_filter = ("department",)
     search_fields = ("name",)
     prepopulated_fields = {"slug": ("name",)}
     fields = ("department", "name", "slug", "image", "description")
     inlines = [
         AboutUsInline,
         SyllabusInline,
         ResultInline,
         StaffMemberInline,
         GalleryImageInline,
         NoticeInline,
         EventInline,
     ]
 

class DepartmentRestrictedAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
         qs = super().get_queryset(request)
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 department = access.department
                 return qs.filter(department=department) | qs.filter(sub_department__department=department, sub_department__isnull=False) | qs.filter(department__isnull=True, sub_department__isnull=True, is_college_wide=True)
             except DepartmentAdminAccess.DoesNotExist:
                 return qs.none()
         return qs
 

     def save_model(self, request, obj, form, change):
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 department = access.department
                 if obj.department and obj.department != department:
                     obj.department = department
                 elif obj.sub_department and obj.sub_department.department != department:
                     obj.sub_department = None # Or handle this as an error
                 elif not obj.department and not obj.sub_department:
                     obj.is_college_wide = True # Default to college-wide if no specific department/sub-department
             except DepartmentAdminAccess.DoesNotExist:
                 pass
         super().save_model(request, obj, form, change)
 

     def has_add_permission(self, request):
         if request.user.is_superuser:
             return True
         try:
             DepartmentAdminAccess.objects.get(user=request.user)
             return True
         except DepartmentAdminAccess.DoesNotExist:
             return False
 

     def has_change_permission(self, request, obj=None):
         if request.user.is_superuser:
             return True
         if obj:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 department = access.department
                 return obj.department == department or (obj.sub_department and obj.sub_department.department == department) or obj.is_college_wide
             except DepartmentAdminAccess.DoesNotExist:
                 return False
         return self.has_add_permission(request)
 

     def has_delete_permission(self, request, obj=None):
         if request.user.is_superuser:
             return True
         if obj:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 department = access.department
                 return obj.department == department or (obj.sub_department and obj.sub_department.department == department)
             except DepartmentAdminAccess.DoesNotExist:
                 return False
         return False
 

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 department = access.department
                 if db_field.name == 'department':
                     kwargs['queryset'] = Department.objects.filter(id=department.id)
                 elif db_field.name == 'sub_department':
                     kwargs['queryset'] = SubDepartment.objects.filter(department=department)
             except DepartmentAdminAccess.DoesNotExist:
                 pass
         return super().formfield_for_foreignkey(db_field, request, **kwargs)
 

 

class SubDepartmentRestrictedAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
         qs = super().get_queryset(request)
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 return qs.filter(sub_department__department=access.department)
             except DepartmentAdminAccess.DoesNotExist:
                 return qs.none()
         return qs
 

     def save_model(self, request, obj, form, change):
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 if obj.sub_department and obj.sub_department.department != access.department:
                     obj.sub_department = None # Or handle as error
             except DepartmentAdminAccess.DoesNotExist:
                 pass
         super().save_model(request, obj, form, change)
 

     def has_add_permission(self, request):
         if request.user.is_superuser:
             return True
         try:
             DepartmentAdminAccess.objects.get(user=request.user)
             return True
         except DepartmentAdminAccess.DoesNotExist:
             return False
 

     def has_change_permission(self, request, obj=None):
         if request.user.is_superuser:
             return True
         if obj:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 return obj.sub_department and obj.sub_department.department == access.department
             except DepartmentAdminAccess.DoesNotExist:
                 return False
         return self.has_add_permission(request)
 

     def has_delete_permission(self, request, obj=None):
         if request.user.is_superuser:
             return True
         if obj:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 return obj.sub_department and obj.sub_department.department == access.department
             except DepartmentAdminAccess.DoesNotExist:
                 return False
         return False
 

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
         if not request.user.is_superuser:
             try:
                 access = DepartmentAdminAccess.objects.get(user=request.user)
                 if db_field.name == 'sub_department':
                     kwargs['queryset'] = SubDepartment.objects.filter(department=access.department)
                 elif db_field.name == 'department':
                     # Prevent sub-department admins from seeing/editing the department
                     kwargs['queryset'] = Department.objects.none()
                     kwargs['widget'] = forms.HiddenInput()
                     if hasattr(kwargs['initial'], 'department'):
                         kwargs['initial'] = kwargs['initial'].department
             except DepartmentAdminAccess.DoesNotExist:
                 pass
         return super().formfield_for_foreignkey(db_field, request, **kwargs)
 

 

@admin.register(Notice)
class NoticeAdmin(DepartmentRestrictedAdmin):
     fields = ['title', 'description', 'is_college_wide', 'department', 'sub_department']
 

@admin.register(Event)
class EventAdmin(DepartmentRestrictedAdmin):
     fields = ['title', 'pdf_upload', 'date', 'time', 'location', 'department', 'sub_department']
 

@admin.register(GalleryImage)
class GalleryImageAdmin(DepartmentRestrictedAdmin):
     fields = ['category', 'title', 'image', 'sub_department']
 

@admin.register(Syllabus)
class SyllabusAdmin(DepartmentRestrictedAdmin):
     fields = ['title', 'file', 'department', 'sub_department']
 

@admin.register(Result)
class ResultAdmin(DepartmentRestrictedAdmin):
     fields = ['title', 'file', 'department', 'sub_department']
 

@admin.register(StaffMember)
class StaffMemberAdmin(DepartmentRestrictedAdmin):
     fields = ['name', 'designation', 'photo', 'email', 'phone', 'department', 'sub_department']
 

 

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
     list_display = ['name']
 

@admin.register(DepartmentAdminAccess)
class DepartmentAdminAccessAdmin(admin.ModelAdmin):
     list_display = [
         "user",
         "department",
         "can_manage_notices",
         "can_manage_gallery",
         "can_manage_syllabus",
         "can_manage_results",
         "can_manage_staff",
     ]
     list_filter = ["department"]
     search_fields = ["user__username", "department__name"]
 

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
     list_display = ('college_name', 'logo')
 

     def has_add_permission(self, request):
         return not SiteSettings.objects.exists()
 

     def has_delete_permission(self, request, obj=None):
         return False
 

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
     list_display = ('__str__', 'sub_department')