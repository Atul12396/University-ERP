from django import forms
from .models import Subject, Student, Timetable, Course, Branch, Semester, Teacher, Payment,Schools,CustomUser,FeeStructure,StudentCertificate

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher','course', 'branches']  # Add other fields if needed

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'profile_picture']



class MarksUploadForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject")
    excel_file = forms.FileField()

    def clean_excel_file(self):
        excel_file = self.cleaned_data['excel_file']
        if not excel_file.name.endswith('.xls') and not excel_file.name.endswith('.xlsx'):
            raise forms.ValidationError("Only Excel files are allowed.")
        return excel_file


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['subject', 'day', 'start_time', 'end_time', 'venue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the subject field queryset to display only subjects relevant to the user or the context
        self.fields['subject'].queryset = Subject.objects.all()  # You can adjust this queryset as needed


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'gender', 'course', 'branch', 'name', 'contact', 'address', 'roll_number', 'student_id', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['branch'].queryset = Branch.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['branch'].queryset = Branch.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['branch'].queryset = self.instance.course.branch_set


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'course']  # Removed 'course' dropdown

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'course', 'branch']  # Removed 'course' and 'branch' dropdowns

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the queryset for 'course' and 'branch' fields
        self.fields['course'].queryset = Course.objects.none()
        self.fields['branch'].queryset = Branch.objects.none()

 
# forms.py


# forms.py
 

from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'course', 'teacher', 'semester', 'branches']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()  # Initialize an empty queryset for courses


 

class AssignStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='student'), empty_label=None, label='Select Student')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course')
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label='Branch')
    school = forms.ModelChoiceField(queryset=Schools.objects.all(), label='School')
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], label='Gender')
    name = forms.CharField(max_length=100, label='Name')
    contact = forms.CharField(max_length=20, label='Contact')
    address = forms.CharField(max_length=255, label='Address')
    roll_number = forms.CharField(max_length=20, label='Roll number')
    student_id = forms.CharField(max_length=20, label='Student id')
    profile_picture = forms.ImageField(label='Profile picture')
    fee_structure = forms.CharField(max_length=100, label='Fee structure')

    def assign_student_role(self):
        student = self.cleaned_data['student']
        student.role = 'student'
        student.course = self.cleaned_data['course']
        student.branch = self.cleaned_data['branch']
        student.school = self.cleaned_data['school']
        student.gender = self.cleaned_data['gender']
        student.name = self.cleaned_data['name']
        student.contact = self.cleaned_data['contact']
        student.address = self.cleaned_data['address']
        student.roll_number = self.cleaned_data['roll_number']
        student.student_id = self.cleaned_data['student_id']
        student.profile_picture = self.cleaned_data['profile_picture']
        student.fee_structure = self.cleaned_data['fee_structure']
        student.save()


from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # You can specify the fields you want to include here

# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['amount']  # Add other relevant fields if needed

#     def calculate_remaining_amount(self, total_amount):
#         total_paid = self.cleaned_data.get('amount', 0)
#         return max(total_amount - total_paid, 0)
    


# class AssignFeeStructureForm(forms.Form):
#     student = forms.ModelChoiceField(queryset=Student.objects.all(), label='Select Student')
#     fee_structure = forms.ModelChoiceField(queryset=FeeStructure.objects.all(), label='Fee Structure')

#     def assign_fee_structure(self):
#         student = self.cleaned_data['student']
#         student.fee_structure = self.cleaned_data['fee_structure']
#         student.save()




class AssignFeeStructureForm(forms.Form):
    fee_structure = forms.ModelChoiceField(queryset=FeeStructure.objects.all(), empty_label="Select Fee Structure")

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'transaction_id', 'payment_method']


class StudentCertificateForm(forms.ModelForm):
    class Meta:
        model = StudentCertificate
        fields = ['student', 'certificate_type', 'certificate_file']

    def __init__(self, *args, **kwargs):
        super(StudentCertificateForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['readonly'] = True



class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'



from django import forms
from .models import Teacher, NonTeachingStaff  # Assuming NonTeachingStaff model exists

class TeacherForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='teacher'), empty_label="Select Teacher")

    class Meta:
        model = Teacher
        fields = ['user', 'designation', 'school', 'department', 'course', 'branch', 'semester', 'subjects', 'name', 'address', 'contact']

class AddNonTeachingStaffForm(forms.ModelForm):
    class Meta:
        model = NonTeachingStaff
        fields = ['name', 'role', 'contact', 'address']


 


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id']
