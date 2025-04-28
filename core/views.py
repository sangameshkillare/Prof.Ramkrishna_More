from django.shortcuts import render, get_object_or_404, redirect
from .models import SiteSettings, SubDepartment, Department, AboutUs, Syllabus, Result, StaffMember, GalleryImage, Notice, Event, GalleryCategory
from .forms import NoticeForm, GalleryImageForm, SyllabusForm, ResultForm, StaffMemberForm


from django.contrib.auth.decorators import login_required
from .models import DepartmentAdminAccess, StaffMember, Department, SubDepartment






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


def manage_gallery(request, sub_dept_id=None):
    if sub_dept_id:
        sub_department = get_object_or_404(SubDepartment, pk=sub_dept_id)
        gallery_images = GalleryImage.objects.filter(sub_department=sub_department)
    else:
        gallery_images = GalleryImage.objects.all()
        sub_department = None
    return render(request, 'core/manage_gallery.html', {'gallery_images': gallery_images, 'sub_department':sub_department})



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





from .models import SiteSettings


def home(request):
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None
    return render(request, 'core/home.html', {'site_settings': site_settings})




# Example for a department page view


from .models import Department, SubDepartment, SiteSettings

def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    subdepartments = SubDepartment.objects.filter(department=department)
    site_settings = None
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None
    return render(request, 'core/department_detail.html', {
        'department': department,
        'subdepartments': subdepartments,
        'site_settings': site_settings
    })
# # You'll need to do this for all your public-facing views


from django.http import JsonResponse
from .models import Department, SubDepartment
from django.core import serializers

def get_departments_subdepartments(request):
    departments = Department.objects.all()
    data = []
    for department in departments:
        subdepartments = SubDepartment.objects.filter(department=department)
        data.append({
            'id': department.id,
            'name': department.name,
            'slug': department.name.lower().replace(' ', '-'), # Basic slug generation
            'subdepartments': [{'id': sub.id, 'name': sub.name, 'slug': f"{department.name.lower().replace(' ', '-')}-{sub.name.lower().replace(' ', '-')}"} for sub in subdepartments]
        })
    return JsonResponse(data, safe=False)





from .models import SiteSettings, Department, SubDepartment



def departments_overview(request):
    departments = Department.objects.all()
    site_settings = None
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None

    context = {
        'departments': departments,
        'site_settings': site_settings,   # Make sure to pass site_settings here!
    }
    return render(request, 'core/departments_overview.html', context) # Adjust template name if needed



def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    subdepartments = SubDepartment.objects.filter(department=department)
    animated_subdepartments = []
    for index, sub_dept in enumerate(subdepartments):
        delay = index * 0.1 + 0.2
        animated_subdepartments.append({'sub_department': sub_dept, 'animation_delay': delay})
    site_settings = None
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None
    return render(request, 'core/department_detail.html', { # Make sure this is the correct template name
        'department': department,
        'animated_subdepartments': animated_subdepartments,
        'site_settings': site_settings
    })




from .models import SiteSettings, SubDepartment, Department, AboutUs, Syllabus, Result, StaffMember, GalleryImage, Notice, Event



def sub_department_detail(request, department_slug, sub_department_slug):
    department = get_object_or_404(Department, slug=department_slug)
    sub_department = get_object_or_404(SubDepartment, slug=sub_department_slug, department=department)
    site_settings = None
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None
    about_us = AboutUs.objects.filter(sub_department=sub_department).first()
    syllabi = Syllabus.objects.filter(sub_department=sub_department) # Removed .order_by('-uploaded_at')
    results = Result.objects.filter(sub_department=sub_department) # Removed .order_by('-uploaded_at')
    staff_members = StaffMember.objects.filter(sub_department=sub_department)
    gallery_images = GalleryImage.objects.filter(sub_department=sub_department)
    notices = Notice.objects.filter(sub_department=sub_department).order_by('-created_at')
    events = Event.objects.filter(sub_department=sub_department).order_by('-date', 'time')

    context = {
        'department': department,
        'sub_department': sub_department,
        'site_settings': site_settings,
        'about_us': about_us,
        'syllabi': syllabi,
        'results': results,
        'staff_members': staff_members,
        'gallery_images': gallery_images,
        'notices': notices,
        'events': events,
    }
    return render(request, 'core/sub_department_detail.html', context)



# core/views.py

from .models import SiteSettings, SubDepartment, Department

def sub_department_about(request, slug):
    try:
        site_settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        site_settings = None
    sub_department = get_object_or_404(SubDepartment, slug=slug)
    department = sub_department.department
    # Fetch about us content related to the sub_department
    return render(request, 'core/sub_department_about.html', {'site_settings': site_settings, 'sub_department': sub_department, 'department': department})

def sub_department_syllabus(request, slug):
    # ... your logic for displaying syllabus
    pass

def sub_department_results(request, slug):
    # ... your logic for displaying results
    pass

def sub_department_staff(request, slug):
    # ... your logic for displaying staff
    pass

def sub_department_gallery(request, slug):
    # ... your logic for displaying gallery
    pass

def sub_department_notices(request, slug):
    # ... your logic for displaying notices
    pass

def sub_department_events(request, slug):
    # ... your logic for displaying events
    pass




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import StaffMember

def staff_detail_api(request, staff_id):
    staff = get_object_or_404(StaffMember, id=staff_id)
    data = {
        'id': staff.id,
        'name': staff.name,
        'designation': staff.designation,
        'photo': staff.photo.url if staff.photo else '',
        'email': staff.email,
        'phone': staff.phone,
        'specialization': staff.specialization,
        'career_summary': staff.career_summary,
        'qualifications': staff.qualifications,
        'mobile_numbers': staff.mobile_numbers,
        'email_addresses': staff.email_addresses,
        'courses_facilitated': staff.courses_facilitated,
        'research_co_supervision': staff.research_co_supervision,
        # 'patents': staff.patents,
        'awards_and_recognition': staff.awards_and_recognition,
        'research_publications': staff.research_publications,
        'professional_activities': staff.professional_activities,
        'work_experience': staff.work_experience,
        # Add other fields as needed
    }
    return JsonResponse(data)




#______________________________new code and functionality__________________________


# core/views.py
from django.shortcuts import render
from .models import StudentDevelopment

def student_development_page(request):
    student_development_data = StudentDevelopment.objects.all()   # Fetch all student development items
    context = {'student_development_data': student_development_data}
    return render(request, 'core/student_development.html', context)


# core/views.py
from django.http import JsonResponse


def student_development_detail_api(request, development_id):
    try:
        development_item = StudentDevelopment.objects.get(pk=development_id)
        data = {
            'id': development_item.id,
            'title': development_item.title,
            'description': development_item.description,
            # Add other fields you want to send
        }
        return JsonResponse(data)
    except StudentDevelopment.DoesNotExist:
        return JsonResponse({'error': 'Student development item not found'}, status=404)



#---------------------new pages adding
from django.shortcuts import render, get_object_or_404
from .models import AboutUsPage, MarqueeImage

def about_us(request):
    """
    View for the About Us page. Fetches content from the database.
    Assumes only one AboutUsPage object exists.
    """
    # Get the first (or only) AboutUsPage instance
    about_page = AboutUsPage.objects.first()

    # Get all active marquee images
    marquee_images = MarqueeImage.objects.filter(is_active=True)

    context = {
        'about_page': about_page,
        'marquee_images': marquee_images,
    }
    return render(request, 'core/about_us.html', context)
