from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_expense_alert_task(user_email, amount, category_name):
    """
    This runs entirely in the background via Redis.
    """
    subject = "High Expense Alert!"
    message = f"Warning: You just recorded a large expense of Rs {amount} for '{category_name}'."
    from_email = "alerts@expensetracker.com"

    send_mail(subject, message, from_email, [user_email], fail_silently=False)

    return f"Success: Alert sent to {user_email}"
