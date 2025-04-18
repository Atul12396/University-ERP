# Final ERP/Final ERP/ERP/myapp/tasks.py

from celery import shared_task
from django.utils import timezone
from registration_app.models import Student, Payment, FeeStructure
from datetime import timedelta

@shared_task
def send_payment_reminders():
    now = timezone.now()
    students = Student.objects.all()
    for student in students:
        fee_structure = student.fee_structure
        if fee_structure:
            last_payment = student.payment_set.order_by('-payment_date').first()
            if last_payment:
                next_due_date = last_payment.payment_date + timedelta(days=fee_structure.frequency_months * 30)
                if now >= next_due_date:
                    # Logic to send reminder (e.g., email, notification)
                    print(f"Reminder sent to {student.name} for payment.")
            else:
                initial_due_date = student.created_at + timedelta(days=fee_structure.frequency_months * 30)
                if now >= initial_due_date:
                    print(f"Initial reminder sent to {student.name} for payment.")

