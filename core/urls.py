from django.urls import path
from . import views

urlpatterns = [
    path('department/dashboard/', views.department_dashboard, name='department_dashboard'),

    path('department/notices/', views.manage_notices, name='manage_notices'),
    path('department/notices/sub/<int:sub_dept_id>/', views.manage_notices, name='manage_sub_department_notices'),
    path('department/notices/add/', views.add_notice, name='add_notice'),
    path('department/notices/add/sub/<int:sub_dept_id>/', views.add_notice, name='add_sub_department_notice'),
    path('department/notices/edit/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('department/notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),

    path('department/gallery/', views.manage_gallery, name='manage_gallery'),
    path('department/gallery/sub/<int:sub_dept_id>/', views.manage_gallery, name='manage_sub_department_gallery'),
    path('department/gallery/add/', views.add_gallery, name='add_gallery'),
    path('department/gallery/add/sub/<int:sub_dept_id>/', views.add_gallery, name='add_sub_department_gallery'),
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
]