from django.db import models
from django.db.models import Q
DONOR = 'DONOR'
LOANER = 'LOANER'


class QarzUser(models.Model):

    USER_TYPE_CHOICES = (
        ('', 'Choose user type'),
        (str(DONOR), DONOR),
        (str(LOANER), LOANER)
    )

    cnic = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)


class Transaction(models.Model):
    amount = models.IntegerField()
    donation_or_loan = models.BooleanField(default=True)
    transaction_date = models.DateTimeField(auto_now_add=True, blank=True)
    qarz_user = models.ForeignKey(QarzUser, on_delete=models.CASCADE)


class Report(models.Model):
    report_user = models.ForeignKey(QarzUser, on_delete=models.CASCADE)
    report_date = models.DateTimeField(null=True, blank=True)
    total_donated = models.IntegerField(blank=True, null=True)
    total_loan = models.IntegerField(blank=True, null=True)
    remaining_loan = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.report_user.type == DONOR:
            user_transactions = Transaction.objects.filter(qarz_user=self.report_user).filter(donation_or_loan=True)
            donations = user_transactions.filter(transaction_date__gte=self.report_date)
            total_donations = 0
            for donation in donations:
                total_donations += donation.amount
            # set the total_donated field
            self.total_donated = total_donations

        elif self.report_user.type == LOANER:
            pass

        super().save(*args, **kwargs)
