from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from library.models import Loan

class Command(BaseCommand):
    help = "Send email notifications for overdue loans."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        overdue_loans = Loan.objects.filter(status="ACTIVE", due_date__lt=today)
        for loan in overdue_loans:
            if not loan.user.email:
                self.stdout.write(self.style.WARNING(f"No email for user {loan.user.username}"))
                continue

            subject = f"Overdue Book Notification: {loan.book.title}"
            message = (
                f"Dear {loan.user.username},\n\n"
                f"Your loan for the book '{loan.book.title}' was due on {loan.due_date} and is now overdue.\n"
                "Please return the book as soon as possible.\n\n"
                "Thank you!"
            )
            try:
                send_mail(subject, message, None, [loan.user.email])
                self.stdout.write(self.style.SUCCESS(f"Notification sent to {loan.user.username}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email to {loan.user.username}: {e}"))
