from django.contrib import admin
#from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget 
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Subject, Student, Attendance, Teacher, AttendanceReport, Course, Timetable, Department, Branch, Semester, HOD, Announcement, FeeStructure, Payment, Schools,StudentCertificate,SS,Hostel,HostelDetails,HostelFees,FinancialFees,Scholarship,Transport,TransportFees,Leave
#from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget 



from django.contrib import admin
from .models import Hostel, HostelDetails




@admin.register(Hostel)  # Register Hostel model
class HostelAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(HostelDetails)  # Automatically registers HostelDetails
class HostelDetailsAdmin(admin.ModelAdmin):
    list_display = ("hostel", "floor", "room_no", "room_type", "sharing", "current_occupancy", "is_available")
    list_filter = ("hostel",)  # Filter rooms by hostel
    search_fields = ("room_no", "hostel__name")  # Enable searching by room number and hostel name
    list_per_page = 20  # Pagination
    autocomplete_fields = ("hostel",)  # Enables autocomplete dropdown for hostel selection

    def current_occupancy(self, obj):
        return obj.current_occupancy()
    current_occupancy.short_description = "Current Occupancy"

    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True  # Show a tick or cross in admin panel







class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'  # You can specify the fields you want to include here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the choices for the user field based on the selected user
        self.fields['user'].queryset = CustomUser.objects.filter(role='teacher')
        instance = kwargs.get('instance')
        
        # Set initial values for fields
        if instance:
            self.fields['course'].initial = instance.course
            self.fields['branch'].initial = instance.branch
            self.fields['semester'].initial = instance.semester
            self.fields['subjects'].initial = instance.subjects.all()
        
        # Set queryset for fields
        self.fields['course'].queryset = Course.objects.all()
        self.fields['branch'].queryset = Branch.objects.all()
        self.fields['semester'].queryset = Semester.objects.all()
        self.fields['subjects'].queryset = Subject.objects.all()


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('user', 'semester', 'branch', 'contact', 'address', 'course','display_subjects')
    raw_id_fields = ['course', 'branch', 'semester', 'subjects']  # Make fields searchable
    search_fields = ['user__username']
    
    def display_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    display_subjects.short_description = 'Subjects'


from django import forms
from .models import Student, CustomUser


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        #exclude = ['subjects']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user'].queryset = CustomUser.objects.filter(role='student')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.transport_status == 'Non-Allocated':
    #         self.fields['transport_name'].widget = forms.HiddenInput()

    #     self.fields['user'].queryset = CustomUser.objects.filter(role='student')

    def clean_user(self):
        username = self.cleaned_data['user'].username
        if Student.objects.filter(user__username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already associated with another student.')
        return self.cleaned_data['user']



 

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'branch', 'roll_number', 'name', 'contact', 'address', 'course')
    raw_id_fields = ['course', 'branch', 'semester']

    
    form = StudentAdminForm

    # class Media:
    #     js = ['js/admin/hide_show_fields.js']

    # def display_subjects(self, obj):
    #     return ", ".join([subject.name for subject in obj.subjects.all()])
    # display_subjects.short_description = 'Subjects'

 


 


 


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [SubjectInline]
    search_fields = ['name'] 

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name'] 

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'  # You can specify the fields you want to include here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the choices for the user field based on the selected user
        self.fields['teacher'].queryset = CustomUser.objects.filter(role='teacher')
        instance = kwargs.get('instance')

class SubjectAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Exclude the 'teacher' field from the form data
        form.cleaned_data.pop('teacher', None)
        super().save_model(request, obj, form, change)
        form = TeacherForm
        list_filter = ['course', 'semester']
        search_fields = ['name'] 


class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'branch')  # Display these fields in the list view
    list_filter = ('course', 'branch')  # Add filters for course and branch
    search_fields = ('name',)

 
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('year', 'amount', 'payment_deadline')
    search_fields = ('year',)
 
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_date')
    search_fields = ('student__username',)

class hodForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'  # You can specify the fields you want to include here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the choices for the user field based on the selected user
        self.fields['user'].queryset = CustomUser.objects.filter(role='hod')
        instance = kwargs.get('instance')

class hodAdmin(admin.ModelAdmin):
        form = hodForm
       
class SSadmin(admin.ModelAdmin):
    list_display = ('user',)
 
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance)
admin.site.register(HOD,hodAdmin)
admin.site.register(AttendanceReport)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Branch)
admin.site.register(Announcement)
admin.site.register(FeeStructure, FeeStructureAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Schools)
admin.site.register(StudentCertificate)
admin.site.register(SS,SSadmin)
admin.site.register(HostelFees)
admin.site.register(FinancialFees)
admin.site.register(Scholarship)
admin.site.register(Transport)
admin.site.register(TransportFees)
admin.site.register(Leave)
admin.site.site_header="RIMT University"

