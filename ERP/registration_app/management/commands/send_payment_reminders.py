# myapp/management/commands/send_payment_reminders.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from registration_app.models import Student, Payment, FeeStructure
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send payment reminders for recurring payments'

    def handle(self, *args, **kwargs):
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
                        self.stdout.write(f"Reminder sent to {student.name} for payment.")
                else:
                    # If there's no payment record, consider sending a reminder
                    # based on some initial criteria or skip
                    initial_due_date = student.created_at + timedelta(days=fee_structure.frequency_months * 30)
                    if now >= initial_due_date:
                        self.stdout.write(f"Initial reminder sent to {student.name} for payment.")
