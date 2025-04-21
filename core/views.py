from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DepartmentAdminAccess, Notice, GalleryCategory, GalleryImage, Syllabus, Result, SubDepartment
from .forms import NoticeForm, GalleryImageForm, SyllabusForm, ResultForm




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DepartmentAdminAccess, StaffMember, Department, SubDepartment
from .forms import StaffMemberForm

@login_required
def manage_staff(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user)
    staff_members = StaffMember.objects.filter(department=department_access.department)
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        staff_members = staff_members.filter(subdepartment=sub_department)
    else:
        staff_members = staff_members.filter(subdepartment__isnull=True) # Staff without specific sub-department
    return render(request, 'core/manage_staff.html', {'staff_members': staff_members, 'can_add': department_access.can_manage_staff, 'sub_dept_id': sub_dept_id})

@login_required
def add_staff(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_staff=True)
    initial_data = {'department': department_access.department}
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        initial_data['subdepartment'] = sub_department

    if request.method == 'POST':
        form = StaffMemberForm(request.POST, request.FILES)
        if form.is_valid():
            staff_member = form.save(commit=False)
            staff_member.department = department_access.department
            staff_member.subdepartment = initial_data.get('subdepartment')
            staff_member.save()
            return redirect('manage_staff', sub_dept_id=sub_dept_id)
    else:
        form = StaffMemberForm(initial=initial_data)
    return render(request, 'core/add_staff.html', {'form': form, 'sub_dept_id': sub_dept_id})

@login_required
def edit_staff(request, staff_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_staff=True)
    staff_member = get_object_or_404(StaffMember, id=staff_id, department=department_access.department)
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, request.FILES, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('manage_staff', sub_dept_id=staff_member.subdepartment_id)
    else:
        form = StaffMemberForm(instance=staff_member)
    return render(request, 'core/edit_staff.html', {'form': form, 'staff_member': staff_member})

@login_required
def delete_staff(request, staff_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_staff=True)
    staff_member = get_object_or_404(StaffMember, id=staff_id, department=department_access.department)
    sub_dept_id = staff_member.subdepartment_id
    if request.method == 'POST':
        staff_member.delete()
        return redirect('manage_staff', sub_dept_id=sub_dept_id)
    return render(request, 'core/delete_confirm.html', {'item_type': 'staff member', 'item': staff_member, 'cancel_url': 'manage_staff', 'sub_dept_id': sub_dept_id})




@login_required
def department_dashboard(request):
    try:
        department_access = DepartmentAdminAccess.objects.get(user=request.user)
        sub_departments = SubDepartment.objects.filter(department=department_access.department)
        return render(request, 'core/department_dashboard.html', {'department': department_access.department, 'sub_departments': sub_departments})
    except DepartmentAdminAccess.DoesNotExist:
        return render(request, 'core/no_access.html')

# Notices CRUD
@login_required
def manage_notices(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user)
    notices = Notice.objects.filter(department=department_access.department)
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        notices = notices.filter(subdepartment=sub_department)
    else:
        notices = notices.filter(is_college_wide=True)
    return render(request, 'core/manage_notices.html', {'notices': notices, 'can_add': department_access.can_manage_notices, 'sub_dept_id': sub_dept_id})

@login_required
def add_notice(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_notices=True)
    initial_data = {'department': department_access.department}
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        initial_data['subdepartment'] = sub_department

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.department = department_access.department
            notice.subdepartment = initial_data.get('subdepartment')
            notice.save()
            return redirect('manage_notices', sub_dept_id=sub_dept_id)
    else:
        form = NoticeForm(initial=initial_data)
    return render(request, 'core/add_notice.html', {'form': form, 'sub_dept_id': sub_dept_id})

@login_required
def edit_notice(request, notice_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_notices=True)
    notice = get_object_or_404(Notice, id=notice_id, department=department_access.department)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('manage_notices', sub_dept_id=notice.subdepartment_id)
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'core/edit_notice.html', {'form': form, 'notice': notice})

@login_required
def delete_notice(request, notice_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_notices=True)
    notice = get_object_or_404(Notice, id=notice_id, department=department_access.department)
    sub_dept_id = notice.subdepartment_id
    if request.method == 'POST':
        notice.delete()
        return redirect('manage_notices', sub_dept_id=sub_dept_id)
    return render(request, 'core/delete_confirm.html', {'item_type': 'notice', 'item': notice, 'cancel_url': 'manage_notices', 'sub_dept_id': sub_dept_id})

# Gallery CRUD
@login_required
def manage_gallery(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user)
    gallery = GalleryImage.objects.filter(department=department_access.department)
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        gallery = gallery.filter(subdepartment=sub_department)
    return render(request, 'core/manage_gallery.html', {'gallery': gallery, 'can_add': department_access.can_manage_gallery, 'sub_dept_id': sub_dept_id})

@login_required
def add_gallery(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_gallery=True)
    initial_data = {'department': department_access.department}
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        initial_data['subdepartment'] = sub_department

    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.department = department_access.department
            gallery_image.subdepartment = initial_data.get('subdepartment')
            gallery_image.save()
            return redirect('manage_gallery', sub_dept_id=sub_dept_id)
    else:
        form = GalleryImageForm(initial=initial_data)
    return render(request, 'core/add_gallery.html', {'form': form, 'sub_dept_id': sub_dept_id})

@login_required
def edit_gallery(request, image_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_gallery=True)
    gallery_image = get_object_or_404(GalleryImage, id=image_id, department=department_access.department)
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=gallery_image)
        if form.is_valid():
            form.save()
            return redirect('manage_gallery', sub_dept_id=gallery_image.subdepartment_id)
    else:
        form = GalleryImageForm(instance=gallery_image)
    return render(request, 'core/edit_gallery.html', {'form': form, 'gallery_image': gallery_image})

@login_required
def delete_gallery(request, image_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_gallery=True)
    gallery_image = get_object_or_404(GalleryImage, id=image_id, department=department_access.department)
    sub_dept_id = gallery_image.subdepartment_id
    if request.method == 'POST':
        gallery_image.delete()
        return redirect('manage_gallery', sub_dept_id=sub_dept_id)
    return render(request, 'core/delete_confirm.html', {'item_type': 'gallery image', 'item': gallery_image, 'cancel_url': 'manage_gallery', 'sub_dept_id': sub_dept_id})

# Syllabus CRUD
@login_required
def manage_syllabus(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user)
    syllabus_list = Syllabus.objects.filter(department=department_access.department)
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        syllabus_list = syllabus_list.filter(subdepartment=sub_department)
    return render(request, 'core/manage_syllabus.html', {'syllabus_list': syllabus_list, 'can_add': department_access.can_manage_syllabus, 'sub_dept_id': sub_dept_id})

@login_required
def add_syllabus(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_syllabus=True)
    initial_data = {'department': department_access.department}
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        initial_data['subdepartment'] = sub_department

    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES)
        if form.is_valid():
            syllabus = form.save(commit=False)
            syllabus.department = department_access.department
            syllabus.subdepartment = initial_data.get('subdepartment')
            syllabus.save()
            return redirect('manage_syllabus', sub_dept_id=sub_dept_id)
    else:
        form = SyllabusForm(initial=initial_data)
    return render(request, 'core/add_syllabus.html', {'form': form, 'sub_dept_id': sub_dept_id})

@login_required
def edit_syllabus(request, syllabus_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_syllabus=True)
    syllabus = get_object_or_404(Syllabus, id=syllabus_id, department=department_access.department)
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES, instance=syllabus)
        if form.is_valid():
            form.save()
            return redirect('manage_syllabus', sub_dept_id=syllabus.subdepartment_id)
    else:
        form = SyllabusForm(instance=syllabus)
    return render(request, 'core/edit_syllabus.html', {'form': form, 'syllabus': syllabus})

@login_required
def delete_syllabus(request, syllabus_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_syllabus=True)
    syllabus = get_object_or_404(Syllabus, id=syllabus_id, department=department_access.department)
    sub_dept_id = syllabus.subdepartment_id
    if request.method == 'POST':
        syllabus.delete()
        return redirect('manage_syllabus', sub_dept_id=sub_dept_id)
    return render(request, 'core/delete_confirm.html', {'item_type': 'syllabus', 'item': syllabus, 'cancel_url': 'manage_syllabus', 'sub_dept_id': sub_dept_id})

# Results CRUD
@login_required
def manage_results(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user)
    results_list = Result.objects.filter(department=department_access.department)
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        results_list = results_list.filter(subdepartment=sub_department)
    return render(request, 'core/manage_results.html', {'results_list': results_list, 'can_add': department_access.can_manage_results, 'sub_dept_id': sub_dept_id})

@login_required
def add_result(request, sub_dept_id=None):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_results=True)
    initial_data = {'department': department_access.department}
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, id=sub_dept_id, department=department_access.department)
        initial_data['subdepartment'] = sub_department

    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.save(commit=False)
            result.department = department_access.department
            result.subdepartment = initial_data.get('subdepartment')
            result.save()
            return redirect('manage_results', sub_dept_id=sub_dept_id)
    else:
        form = ResultForm(initial=initial_data)
    return render(request, 'core/add_result.html', {'form': form, 'sub_dept_id': sub_dept_id})

@login_required
def edit_result(request, result_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_results=True)
    result = get_object_or_404(Result, id=result_id, department=department_access.department)
    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES, instance=result)
        if form.is_valid():
            form.save()
            return redirect('manage_results', sub_dept_id=result.subdepartment_id)
    else:
        form = ResultForm(instance=result)
    return render(request, 'core/edit_result.html', {'form': form, 'result': result})

@login_required
def delete_result(request, result_id):
    department_access = get_object_or_404(DepartmentAdminAccess, user=request.user, can_manage_results=True)
    result = get_object_or_404(Result, id=result_id, department=department_access.department)
    sub_dept_id = result.subdepartment_id
    if request.method == 'POST':
        result.delete()
        return redirect('manage_results', sub_dept_id=sub_dept_id)
    return render(request, 'core/delete_confirm.html', {'item_type': 'result', 'item': result, 'cancel_url': 'manage_results', 'sub_dept_id': sub_dept_id})