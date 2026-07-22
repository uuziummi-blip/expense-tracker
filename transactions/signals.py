from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Transaction, UserBalance
from django.core.cache import cache
from .tasks import send_expense_alert_task


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_user_balance(sender, instance, **kwargs):
    user_balance, created = UserBalance.objects.get_or_create(user=instance.user)

    income = (
        Transaction.objects.filter(
            user=instance.user, category__type="Income"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    expense = (
        Transaction.objects.filter(
            user=instance.user, category__type="Expense"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    user_balance.total_income = income
    user_balance.total_expense = expense
    user_balance.balance = income - expense
    user_balance.save()

    # Trigger an email if a single expense is greater than Rs 5000
    if instance.category.type == "Expense" and instance.amount > 5000:
        # Check if the user actually has an email saved in the database
        if instance.user.email:
            # 2. Use .delay() to send the job to Redis in the background!
            send_expense_alert_task.delay(
                instance.user.email, instance.amount, instance.category.name
            )
            print(
                f"--> ALARM: Task sent to background queue for {instance.user.email}!"
            )
        else:
            print(
                f"--> ALARM SKIPPED: {instance.user.username} does not have an email address set."
            )
