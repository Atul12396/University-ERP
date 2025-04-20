"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from registration_app import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from registration_app.views import create_timetable_no_branch, create_timetable_with_branch, hod_dashboard,student_section_dashboard,account_section,assign_fee_structure,pay_fees,select_course,select_program,select_semester,list_students,edit_student,apply_leave,manage_leave_request,hod_leave_requests,teacher_leave_status

urlpatterns = [

    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('hod-dashboard/', views.hod_dashboard, name='hod-dashboard'),
    path('', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('login/', views.custom_login, name='login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('mark_attendance/<int:subject_id>/', views.mark_attendance, name='mark_attendance'),
    path('student_attendance/', views.student_attendance, name='student_attendance'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('success_page/', views.success_page, name='success_page'),
    path('subject_details/<int:subject_id>/', views.subject_details, name='subject_details'),
    path('student/<int:student_id>/', views.student_details, name='student_details'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('all_subjects/', views.all_subjects, name='all_subjects'),
    path('download_attendance_report/<int:subject_id>/<str:date_from>/<str:date_to>/', views.download_attendance_report, name='download_attendance_report'),
    path('subject_attendance/<int:subject_id>/', views.subject_attendance, name='subject_attendance'),
    path('upload-marks/', views.upload_marks, name='upload_marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
    path('courses/', views.view_courses, name='view_courses'),
    path('courses/<int:course_id>/semesters/', views.view_semesters_no_branch, name='view_semesters_no_branch'),
    path('courses/<int:course_id>/semesters/<int:semester_id>/subjects/', views.view_subjects_no_branch, name='view_subjects_no_branch'),
    path('courses/<int:course_id>/semesters/<int:semester_id>/subjects/<int:subject_id>/create_timetable/', views.create_timetable_no_branch, name='create_timetable_no_branch'),
    
    path('student/announcements/', views.student_announcements, name='student_announcements'),
    path('teacher/announcements/', views.teacher_announcements, name='teacher_announcements'),
    path('apply-leave/', apply_leave, name='teacher_apply_leave'),

    path('view-fees/', views.view_fees, name='view_fees'),
    path('pay_fees/', views.pay_fees, name='pay_fees'),

   
    
    # For courses with branches
    path('courses/<int:course_id>/', views.view_branches, name='view_branches'),
    path('courses/<int:course_id>/<int:branch_id>/semesters/', views.view_semesters, name='view_semesters'),
    path('courses/<int:course_id>/<int:branch_id>/<int:semester_id>/subjects/', views.view_subjects, name='view_subjects'),
    path('courses/<int:course_id>/<int:branch_id>/<int:semester_id>/subjects/<int:subject_id>/create_timetable/', views.create_timetable_with_branch, name='create_timetable_with_branch'),

    # Other URLs
    path('timetable_success/', views.timetable_success, name='timetable_success'),
    path('timetable/', views.view_timetable, name='view_timetable'),


    #hod urls
    
    path('students/', views.hod_students, name='hod-students'),
    path('students/', views.hod_students, name='hod-students'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),
    path('branches/', views.hod_branches, name='hod-branches'),
    path('edit-branch/<int:branch_id>/', views.edit_branch, name='edit_branch'),
    path('subjects/', views.hod_subjects, name='hod-subjects'),
    path('add-subject/', views.add_subject, name='add-subject'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('semesters/', views.hod_semesters, name='hod-semesters'),
    path('edit-semester/<int:semester_id>/', views.edit_semester, name='edit_semester'),
    path('hod-techers/', views.hod_teachers, name='hod-teachers'),
    path('hod/leaves/', hod_leave_requests, name='hod_leave_requests'),
    path('hod/manage_leave_request/<int:leave_id>/<str:action>/', manage_leave_request, name='manage_leave_request'),
    path('teacher/leave-status/', teacher_leave_status, name='teacher_leave_status'),



    path('student_section/', student_section_dashboard, name='student_section_dashboard'),
    path('add_student/', views.add_student, name='add_student'),
    path('account_section/', account_section, name='account_section'),
    path('assign_fee_structure/<int:student_id>/', assign_fee_structure, name='assign_fee_structure'),
    path('pay_fees/<int:student_id>/', pay_fees, name='pay_fees'),
    path('add_student_certificate/', views.add_student_certificate, name='add_student_certificate'),
    

    path('add_student_certificate/', views.add_student_certificate, name='add_student_certificate'),
    path('students_with_documents/', views.student_documents_list, name='student_documents_list'),
    path('students_with_documents/<int:student_id>/', views.student_documents_detail, name='student_documents_detail'),
    path('delete_certificate/<int:certificate_id>/', views.delete_certificate, name='delete_certificate'),


  
   
    path('branches/<int:course_id>/', views.branch_list, name='branch_list'),
    path('semesters/<int:branch_id>/', views.semester_list, name='semester_list'),
    path('students/<int:semester_id>/', views.semester_student_list, name='semester_student_list'),
    path('update_student/<int:student_id>/', views.update_student, name='update_student'),




     path('select_course/', select_course, name='select_course'),
     path('select_program/<int:course_id>/', select_program, name='select_program'),
     path('select_semester/<int:program_id>/', select_semester, name='select_semester'),
     path('list_students/<int:semester_id>/', list_students, name='list_students'),


    path('update_student_view/', views.update_student_view, name='update_student_view'),
    path('edit-student/<int:student_id>/', edit_student, name='edit_student'),


    #HR URL
    path('hr-admin/', views.hr_admin_dashboard, name='hr_admin_dashboard'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-non-teaching-staff/', views.add_non_teaching_staff, name='add_non_teaching_staff'),


    path('feesassign/',views.get_student_fees)

 

 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
