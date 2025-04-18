from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='announcements/', null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Schools(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class Department(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"

class Branch(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):

        return self.name
    


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, blank=True)
    roll_number = models.CharField(max_length=60, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if 'student' in self.email:
            self.role = 'student'
        elif 'teacher' in self.email:
            self.role = 'teacher'
        elif 'hod' in self.email:
            self.role = 'hod'
        elif 'ss' in self.email:
            self.role = 'ss'
        elif 'as' in self.email:
            self.role = 'as'
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() if full_name.strip() else self.username



class HOD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class SS(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class FeeStructure(models.Model):
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    frequency_months = models.IntegerField(default=6)
    payment_deadline = models.DateField(default=0)

    def __str__(self):
        return f"Fee Structure for {self.year}"





class Subject(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)  # Nullable teacher
    total_classes = models.PositiveIntegerField(default=0)
    subject_id = models.CharField(max_length=60, default='', null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    branches = models.ManyToManyField(Branch, related_name='subjects')

    def __str__(self):
        return self.name





class Hostel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()

    def remaining_capacity(self):
        """Calculate available slots in the hostel"""
        total_allocated = sum(room.current_occupancy() for room in self.hostel_details.all())
        return self.capacity - total_allocated

    def __str__(self):
        return f"{self.name} (Capacity Left: {self.remaining_capacity()})"
    
class Transport(models.Model):
    Route = models.CharField(max_length=20)
    Bus_No = models.CharField(max_length=20)

    def __str__(self):
        return f"Route: {self.Route} (Bus No: {self.Bus_No})"



class HostelDetails(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="hostel_details")
    floor = models.PositiveIntegerField()
    room_no = models.PositiveIntegerField()
    room_type = models.CharField(max_length=50, choices=[("AC", "AC"), ("Non-AC", "Non-AC")])
    sharing = models.PositiveIntegerField()  # Max students allowed in the room

    def current_occupancy(self):
        """Count students currently assigned to this room"""
        return self.students.count()

    def is_available(self):
        """Check if room has available slots"""
        return self.current_occupancy() < self.sharing

    def __str__(self):
        return f"Room {self.room_no} - {self.room_type} ({self.current_occupancy()}/{self.sharing} occupied)"



class HostelFees(models.Model):
    hostel_details = models.ForeignKey('HostelDetails', on_delete=models.CASCADE)  # Link to HostelDetails
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store hostel fees

    def __str__(self):
        return f"{self.hostel_details.hostel.name} - {self.hostel_details.room_type} ({self.hostel_details.sharing}) - ₹{self.fee_amount}"
    
class TransportFees(models.Model):
    transport_fees = models.ForeignKey(Transport,on_delete=models.CASCADE)
    fees_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.transport_fees.Route} - ₹{self.fees_amount}"


class FinancialFees(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)  # Link with School
    program = models.ForeignKey(Course, on_delete=models.CASCADE,default=None)  # Link with Program
    registration_fees = models.DecimalField(max_digits=10, decimal_places=2)  # One-time fees
    academic_fees = models.DecimalField(max_digits=10, decimal_places=2)  # Recurring fees
    hostel_fees = models.ForeignKey(HostelFees, on_delete=models.SET_NULL, null=True, blank=True)  # Link with hostel fees
    transport_fees = models.ForeignKey(TransportFees,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.school.name} - {self.program.name} Fees"
    


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='students')
    name = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=20, default='')
    address = models.TextField(default='')
    roll_number = models.CharField(max_length=20, blank=True)
    student_id = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    fee_structure = models.ForeignKey(FinancialFees, on_delete=models.SET_NULL, null=True, blank=True)  # Link to fees

    payment_status = models.BooleanField(default=False)
    
    hostel_room = models.ForeignKey(HostelDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    transport_fees = models.ForeignKey(TransportFees, on_delete=models.SET_NULL, null=True, blank=True)

    
    # Move miscellaneous fees and fine fees to Student
    miscellaneous_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    fees_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def get_total_fees(self):
        """Calculate total fees after discounts"""
        total_fees = 0
        if self.fee_structure:
            total_fees += self.fee_structure.registration_fees
            total_fees += self.fee_structure.academic_fees
            if self.fee_structure.hostel_fees:
                total_fees += self.fee_structure.hostel_fees.amount
        
        total_fees += self.miscellaneous_fees + self.fees_fine

        # Apply scholarship discount
        scholarship = Scholarship.objects.filter(student=self).first()
        if scholarship:
            total_fees -= scholarship.discount_amount  # Reduce fees

        return max(total_fees, 0)  # Ensure it never goes negative

    def get_paid_amount(self):
        """Calculate total amount paid by the student"""
        return Payment.objects.filter(student=self, status="Completed").aggregate(total_paid=Sum('amount'))['total_paid'] or 0

    def get_due_amount(self):
        """Calculate remaining amount to be paid"""
        return max(self.get_total_fees() - self.get_paid_amount(), 0)

    def assign_hostel_fees(self):
        """Assign hostel fees automatically based on the fee structure"""
        if self.fee_structure and self.hostel_room:
            hostel_details = self.hostel_room
            hostel_fee = HostelFees.objects.filter(hostel_details=hostel_details).first()
            if hostel_fee:
                self.fee_structure.hostel_fees = hostel_fee
                self.fee_structure.save()

    def save(self, *args, **kwargs):
        """Override save method to auto-assign hostel fees when fee structure is assigned"""
        if self.fee_structure and not self.hostel_room:
            # Auto-assign hostel based on the fee structure room type (AC/Non-AC)
            hostel_details = HostelDetails.objects.filter(room_type=self.fee_structure.hostel_fees.hostel_details.room_type).first()
            if hostel_details:
                self.hostel_room = hostel_details
        super().save(*args, **kwargs)
        self.assign_hostel_fees()  # Ensure hostel fees are assigned after saving the student



    
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200, null=True, blank=True)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    is_assigned = models.BooleanField(default=False)  # New field to track assignment status

    casual_leaves = models.PositiveIntegerField(default=1)  # 1 per month
    medical_leaves = models.PositiveIntegerField(default=2)  # 2 per quarter
    official_duty_leaves = models.PositiveIntegerField(default=0)
    compass_leaves = models.PositiveIntegerField(default=0)
    special_leaves = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() if self.user else 'No User'


class Leave(models.Model):
    LEAVE_TYPES = [
        ('Casual', 'Casual Leave'),
        ('Medical', 'Medical Leave'),
        ('Official Duty', 'Official Duty Leave'),
        ('Compass', 'Compass Leave'),
        ('Special', 'Special Leave'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(HOD, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.leave_type} ({self.status})"




class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    students = models.ManyToManyField(Student, through='AttendanceReport')
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)



class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)  # Monday, Tuesday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course} - {self.branch} - {self.semester} - {self.subject} - {self.day}"
    

class Marks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=50, null=True, blank=True)
    roll_number = models.CharField(max_length=50, null=True, blank=True)
    semester = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    student_name = models.CharField(max_length=255, null=True, blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exam_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.subject.name} - {self.semester}"

 
 

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Keep ForeignKey
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.CharField(
        max_length=50, 
        choices=[('Online', 'Online'), ('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer')]
    )
    transaction_id = models.CharField(max_length=100, unique=True)  
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], 
        default='Pending'
    )
    payment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.student.student_id} - {self.amount} ({self.status})"


    

class Scholarship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to student
    name = models.CharField(max_length=100)  # Scholarship Name
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount discounted
    granted_by = models.CharField(max_length=100)  # Authority granting the scholarship
    date_granted = models.DateField(auto_now_add=True)  # Date of approval

    def __str__(self):
        return self.student



class StudentCertificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100)
    certificate_file = models.FileField(upload_to='certificates/')


 

class NonTeachingStaff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)  # e.g., Accountant, Clerk, etc.
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_avatar = models.ImageField(upload_to='non_teaching_staff_profile/', null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name






