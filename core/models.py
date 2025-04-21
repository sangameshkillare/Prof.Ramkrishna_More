from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Assigned User")

    def __str__(self):
        return self.name

class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('department', 'name')

    def __str__(self):
        return f"{self.department.name} - {self.name}"

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
    description = RichTextField()
    is_college_wide = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Syllabus(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='syllabus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Result(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='results/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StaffMember(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='staff/', blank=True, null=True)
    bio = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name