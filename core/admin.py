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

from django.contrib import admin
from django.contrib.admin import AdminSite

# Option 1: Basic customization
admin.site.site_header = "Prof.Ramkrishna More Admin-Portal"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Dashboard"
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.db import models


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
                base_filters = models.Q(department=department) | models.Q(sub_department__department=department, sub_department__isnull=False)

                if self.model == Notice:
                    return qs.filter(base_filters | models.Q(department__isnull=True, sub_department__isnull=True, is_college_wide=True))
                elif self.model == GalleryImage:
                    return qs.filter(sub_department__department=department)
                else:
                    return qs.filter(base_filters)
            except DepartmentAdminAccess.DoesNotExist:
                return qs.none()
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            try:
                access = DepartmentAdminAccess.objects.get(user=request.user)
                department = access.department
                if hasattr(obj, 'department') and obj.department and obj.department != department:
                    obj.department = department
                elif hasattr(obj, 'sub_department') and obj.sub_department and obj.sub_department.department != department:
                    obj.sub_department = None
                elif hasattr(obj, 'is_college_wide') and not obj.department and not obj.sub_department:
                    obj.is_college_wide = True
                elif hasattr(obj, 'sub_department') and obj.sub_department and not hasattr(obj, 'department'):
                    obj.department = obj.sub_department.department
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
                return (hasattr(obj, 'department') and obj.department == department) or \
                       (hasattr(obj, 'sub_department') and obj.sub_department and obj.sub_department.department == department)
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
                return (hasattr(obj, 'department') and obj.department == department) or \
                       (hasattr(obj, 'sub_department') and obj.sub_department and obj.sub_department.department == department)
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



@admin.register(Notice)
class NoticeAdmin(DepartmentRestrictedAdmin):
    fields = ['title', 'description', 'is_college_wide', 'department', 'sub_department', 'pdf_upload']  # Add 'pdf_upload' here


@admin.register(Syllabus)
class SyllabusAdmin(DepartmentRestrictedAdmin):
    fields = ['title', 'file', 'pdf_upload', 'department', 'sub_department']


@admin.register(Result)
class ResultAdmin(DepartmentRestrictedAdmin):
    fields = ['title', 'file', 'department', 'sub_department']

from django.contrib import admin
from .models import StaffMember
from .forms import StaffMemberForm  # Import your custom form

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'sub_department']
    form = StaffMemberForm  # Tell the admin to use your custom form
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'designation', 'photo', 'email', 'phone', 'department', 'sub_department')
        }),
        ('Academic Details', {
            'fields': ('specialization', 'career_summary', 'qualifications_normal')
        }),
        ('Contact Information', {
            'fields': ('mobile_numbers_normal', 'email_addresses_normal')
        }),
        ('Research Activities', {
            'fields': ('research_co_supervision_normal', 'research_publications')
        }),
        ('Professional Activities', {
            'fields': ('awards_and_recognition_normal', 'professional_activities_normal', 'work_experience')
        }),
    )

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


@admin.register(Event)
class EventAdmin(DepartmentRestrictedAdmin):
    fields = ['title', 'pdf_upload', 'date', 'time', 'location', 'department', 'sub_department']
    list_display = ('title', 'date', 'sub_department', 'department')
    list_filter = ('sub_department', 'department')
    search_fields = ('title', 'location')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            try:
                access = DepartmentAdminAccess.objects.get(user=request.user)
                department = access.department
                return qs.filter(department=department) | qs.filter(sub_department__department=department, sub_department__isnull=False)
            except DepartmentAdminAccess.DoesNotExist:
                return qs.none()
        return qs

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


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sub_department')  # Customize the list view in the admin panel
    list_filter = ('category', 'sub_department')  # Add filters for easier management
    search_fields = ('title',)  # Enable searching by title
    



#---------------------nrew pages adding


# from .models import WebsiteAboutUs

# @admin.register(WebsiteAboutUs)
# class WebsiteAboutUsAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     fields = ('title', 'content')

from django.contrib import admin
from .models import AboutUsPage, MarqueeImage
from django.utils.html import format_html

@admin.register(AboutUsPage)
class AboutUsPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'content', 'image')
        }),
        ('History Section', {
            'fields': ('history_title', 'history_content'),
            'classes': ('collapse',)
        }),
        ('Mission Section', {
            'fields': ('mission_title', 'mission_content'),
            'classes': ('collapse',)
        }),
        ('Vision Section', {
            'fields': ('vision_title', 'vision_content'),
            'classes': ('collapse',)
        }),
    )

    def short_content_display(self, obj):
        return obj.short_content()
    short_content_display.short_description = 'Short Content'

    readonly_fields = ('short_content_display',)
    list_display = ('title', 'short_content_display')
    search_fields = ('title',)  # Optional to include 'content'

@admin.register(MarqueeImage)
class MarqueeImageAdmin(admin.ModelAdmin):
    list_display = ('admin_image', 'alt_text', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('admin_image',)

    def admin_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 5px;" />', obj.image.url)
        return 'No Image'
    admin_image.short_description = 'Image Preview'
