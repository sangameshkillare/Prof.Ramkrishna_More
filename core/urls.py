from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path('departments/<slug:department_slug>/<slug:sub_department_slug>/', views.sub_department_detail, name='sub_department_detail'),
    path('department/notices/', views.manage_notices, name='manage_notices'),
    path('department/notices/sub/<int:sub_dept_id>/', views.manage_notices, name='manage_sub_department_notices'),
    path('department/notices/add/', views.add_notice, name='add_notice'),
    path('department/notices/add/sub/<int:sub_dept_id>/', views.add_notice, name='add_sub_department_notice'),
    path('department/notices/edit/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('department/notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('department/gallery/', views.manage_gallery, name='manage_gallery'),
    path('department/gallery/sub/<int:sub_dept_id>/', views.manage_gallery, name='manage_sub_department_gallery'),
    path('department/gallery/edit/<int:image_id>/', views.edit_gallery, name='edit_gallery'),
    path('department/gallery/delete/<int:image_id>/', views.delete_gallery, name='delete_gallery'),
    path('department/syllabus/', views.manage_syllabus, name='manage_syllabus'),
    path('department/syllabus/sub/<int:sub_dept_id>/', views.manage_syllabus, name='manage_sub_department_syllabus'),
    path('department/syllabus/add/', views.add_syllabus, name='add_syllabus'),
    path('department/syllabus/add/sub/<int:sub_dept_id>/', views.add_syllabus, name='add_sub_department_syllabus'),
    path('department/syllabus/edit/<int:syllabus_id>/', views.edit_syllabus, name='edit_syllabus'),
    path('department/syllabus/delete/<int:syllabus_id>/', views.delete_syllabus, name='delete_syllabus'),
    path('department/results/', views.manage_results, name='manage_results'),
    path('department/results/sub/<int:sub_dept_id>/', views.manage_results, name='manage_sub_department_results'),
    path('department/results/add/', views.add_result, name='add_result'),
    path('department/results/add/sub/<int:sub_dept_id>/', views.add_result, name='add_sub_department_result'),
    path('department/results/edit/<int:result_id>/', views.edit_result, name='edit_result'),
    path('department/results/delete/<int:result_id>/', views.delete_result, name='delete_result'),
    path('department/staff/', views.manage_staff, name='manage_staff'),
    path('department/staff/sub/<int:sub_dept_id>/', views.manage_staff, name='manage_sub_department_staff'),
    path('department/staff/add/', views.add_staff, name='add_staff'),
    path('department/staff/add/sub/<int:sub_dept_id>/', views.add_staff, name='add_sub_department_staff'),
    path('department/staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('department/staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    # Public Facing URLs
    path('departments/', views.departments_overview, name='departments_overview'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),
    path('sub-departments/<slug:slug>/', views.sub_department_detail, name='sub_department_detail'),
    # Public Facing URLs for specific sub-department content
    path('sub-departments/<slug:slug>/about/', views.sub_department_about, name='sub_department_about'),
    path('sub-departments/<slug:slug>/syllabus/', views.sub_department_syllabus, name='sub_department_syllabus'),
    path('sub-departments/<slug:slug>/results/', views.sub_department_results, name='sub_department_results'),
    path('sub-departments/<slug:slug>/staff/', views.sub_department_staff, name='sub_department_staff'),
    path('sub-departments/<slug:slug>/gallery/', views.sub_department_gallery, name='sub_department_gallery'),
    path('sub-departments/<slug:slug>/notices/', views.sub_department_notices, name='sub_department_notices'),
    path('sub-departments/<slug:slug>/events/', views.sub_department_events, name='sub_department_events'),
    # API endpoint  
    path('api/staff/<int:staff_id>/', views.staff_detail_api, name='staff_detail_api'),
    path('api/departments-subdepartments/', views.get_departments_subdepartments, name='get_departments_subdepartments'),
    #______________________new code and functionality
    path('about/', views.about_us, name='about_us'),

    path('api/student-development/<int:development_id>/', views.student_development_detail_api, name='student_development_detail_api'),
    path('student-development/', views.student_development_page, name='student_development_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

