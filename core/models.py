from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField



class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # ... other fields (if any)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sub_departments')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sub_department_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.department.name}-{self.name}")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('department', 'slug')

    def __str__(self):
        return self.name
    

class AboutUs(models.Model):
    sub_department = models.OneToOneField(SubDepartment, related_name='about_us', on_delete=models.CASCADE)
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
    sub_department = models.ForeignKey(SubDepartment, related_name='notices', on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, related_name='notices', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_college_wide = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    sub_department = models.ForeignKey(SubDepartment, related_name='gallery_images', on_delete=models.CASCADE)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image - {self.id}"

class Syllabus(models.Model):
    sub_department = models.ForeignKey(SubDepartment, related_name='syllabi', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='syllabi', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='syllabi/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.sub_department.name}"

class Result(models.Model):
    sub_department = models.ForeignKey(SubDepartment, related_name='results', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='results', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='results/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.sub_department.name}"




class StaffMember(models.Model):
    sub_department = models.ForeignKey(SubDepartment, related_name='staff_members', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, related_name='staff', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # ... other staff details

    def __str__(self):
        return self.name
    
    
    
    
    
    
    

class SiteSettings(models.Model):
    college_name = models.CharField(max_length=255, default="Your College Name")
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
    sub_department = models.ForeignKey(SubDepartment, related_name='events', on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, related_name='events', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    pdf_upload = models.FileField(upload_to='event_pdfs/', blank=True, null=True) # Example FileField
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
    