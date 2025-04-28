from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


from ckeditor.fields import RichTextFormField       # For forms

from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='sub_departments')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sub_department_images/', blank=True,
                               null=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,
                                      null=True,
                                      related_name='managed_sub_departments')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.department.name}-{self.name}")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('department', 'slug')

    def __str__(self):
        return self.name


class AboutUs(models.Model):
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE)
    content = RichTextUploadingField()

    def __str__(self):
        return f"About Us - {self.sub_department.name}"


class DepartmentAdminAccess(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    can_manage_notices = models.BooleanField(default=False)
    can_manage_gallery = models.BooleanField(default=False)
    can_manage_syllabus = models.BooleanField(default=False)
    can_manage_results = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Department Admin Access"
        unique_together = ('user', 'department')

    def __str__(self):
        return f"{self.user.username} - {self.department.name}"


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_college_wide = models.BooleanField(default=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE,
                                   null=True, blank=True)
    sub_department = models.ForeignKey('SubDepartment', on_delete=models.CASCADE,
                                       null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf_upload = models.FileField(upload_to='notices/pdfs/', null=True,
                                  blank=True)  # New PDF field

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
from django.utils import timezone

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery_images/')
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now) # Added uploaded_at

    def __str__(self):
        return self.title

class Syllabus(models.Model):
    sub_department = models.ForeignKey('SubDepartment', on_delete=models.CASCADE,
                                       null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE,
                                     null=True, blank=True)
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='syllabi/')  # Existing file field (you can rename if needed)
    pdf_upload = models.FileField(upload_to='syllabi/pdfs/', null=True,
                                  blank=True)  # New PDF field

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Syllabi"


class Result(models.Model):
    sub_department = models.ForeignKey('SubDepartment', on_delete=models.CASCADE,
                                       null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE,
                                     null=True, blank=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='results/')
    uploaded_at = models.DateTimeField(
        auto_now_add=True)  # Add this field

    def __str__(self):
        return self.title


from django.db import models
from .models import Department, SubDepartment


class StaffMember(models.Model):
    sub_department = models.ForeignKey(SubDepartment,
                                       related_name='staff_members',
                                       on_delete=models.SET_NULL, null=True,
                                       blank=True)
    department = models.ForeignKey(Department, related_name='staff',
                                     on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # patents = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    career_summary = models.TextField(blank=True, null=True)
    qualifications = models.CharField(max_length=500, blank=True,
                                      null=True)  # Added max_length
    mobile_numbers = models.CharField(max_length=255, blank=True,
                                      null=True)  # Added max_length
    email_addresses = models.TextField(blank=True, null=True)
    courses_facilitated = models.CharField(max_length=500, blank=True,
                                           null=True)  # Added max_length
    research_co_supervision = models.TextField(blank=True, null=True)
    # patents = models.TextField(blank=True, null=True)
    awards_and_recognition = models.TextField(blank=True, null=True)
    research_publications = models.TextField(blank=True, null=True)
    professional_activities = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    college_name = models.CharField(max_length=255,
                                    default="Your College Name")
    logo = models.ImageField(upload_to='site_logo/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise Exception("Only one SiteSettings instance can exist")
        return super().save(*args, **kwargs)


class Event(models.Model):
    sub_department = models.ForeignKey(SubDepartment, related_name='events',
                                       on_delete=models.CASCADE, blank=True,
                                       null=True)
    department = models.ForeignKey(Department, related_name='events',
                                     on_delete=models.CASCADE, blank=True,
                                     null=True)
    title = models.CharField(max_length=255)
    pdf_upload = models.FileField(upload_to='event_pdfs/', blank=True,
                                  null=True)  # Example FileField
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SubDepartmentAdminAccess(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE)
    can_manage_notices = models.BooleanField(default=False)
    can_manage_gallery = models.BooleanField(default=False)
    can_manage_syllabus = models.BooleanField(default=False)
    can_manage_results = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Sub-Department Admin Access"
        unique_together = ('user', 'sub_department')

    def __str__(self):
        return f"{self.user.username} - {self.sub_department.name}"

class StudentDevelopment(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    # Add other relevant fields like image, date, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                         null=True,
                                         blank=True)  # Added uploaded_at

    def __str__(self):
        return self.title
# __________________________________new pages and functionality_______________

# from ckeditor_uploader.fields import RichTextUploadingField
# class WebsiteAboutUs(models.Model):
#     title = models.CharField(max_length=255, default="About Us")
#     content = RichTextUploadingField()

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = "Website About Us"
from django.db import models
from django.utils.text import Truncator
from ckeditor.fields import RichTextField  # Correct import

class AboutUsPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Page Title")
    content = RichTextField(verbose_name="Page Content") 

    history_title = models.CharField(max_length=255, verbose_name="History Title", blank=True, null=True)
    history_content = RichTextField(verbose_name="History Content", blank=True, null=True)

    mission_title = models.CharField(max_length=255, verbose_name="Mission Title", blank=True, null=True)
    mission_content = RichTextField(verbose_name="Mission Content", blank=True, null=True)

    vision_title = models.CharField(max_length=255, verbose_name="Vision Title", blank=True, null=True)
    vision_content = RichTextField(verbose_name="Vision Content", blank=True, null=True)
    
    image = models.ImageField(upload_to='about_us_images/', verbose_name="Main Image", blank=True, null=True)

    class Meta:
        verbose_name = "About Us Page"
        verbose_name_plural = "About Us Pages"

    def __str__(self):
        return self.title

    def short_content(self):
        return Truncator(self.content).chars(200, truncate='...')
    short_content.allow_tags = True


class MarqueeImage(models.Model):
    image = models.ImageField(upload_to='marquee_images/', verbose_name="Marquee Image")
    alt_text = models.CharField(max_length=255, verbose_name="Image Alt Text", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Marquee Image"
        verbose_name_plural = "Marquee Images"
        ordering = ('id',)

    def __str__(self):
        return f"Marquee Image {self.id}"
