from django.db import models
from django.db.models import Q
DONOR = 'DONOR'
LOANER = 'LOANER'
DONATION = 'DONATION'
LOAN = 'LOAN'
RETURN = 'RETURN'


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

    def __str__(self):
        return self.name


class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = (
        ('', 'Transaction type'),
        (str(DONATION), DONATION),
        (str(LOAN), LOAN),
        (str(RETURN), RETURN)
    )

    amount = models.IntegerField()
    type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=20, default=DONATION)
    transaction_date = models.DateTimeField(auto_now_add=True, blank=True)
    qarz_user = models.ForeignKey(QarzUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.qarz_user.name


class Report(models.Model):
    report_user = models.ForeignKey(QarzUser, on_delete=models.CASCADE)
    report_date = models.DateTimeField(null=True, blank=True)
    total_donated = models.IntegerField(blank=True, null=True)
    total_loan = models.IntegerField(blank=True, null=True)
    remaining_loan = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.report_user.name

    def save(self, *args, **kwargs):
        if self.report_user.type == DONOR:
            user_transactions = Transaction.objects.filter(qarz_user=self.report_user).filter(type=DONATION)
            filtered_donations = user_transactions.filter(transaction_date__lte=self.report_date)
            total_donations = 0
            for donation in filtered_donations:
                total_donations += donation.amount
            # set the total_donated field
            self.total_donated = total_donations

        elif self.report_user.type == LOANER:
            user_loans = Transaction.objects.filter(qarz_user=self.report_user).filter(type=LOAN)
            loans = user_loans.filter(transaction_date__lte=self.report_date)
            total_loans = 0
            for loan in loans:
                total_loans += loan.amount
            # set the total_loan field
            self.total_loan = total_loans

            user_returns = Transaction.objects.filter(qarz_user=self.report_user).filter(type=RETURN)
            filtered_returns = user_returns.filter(transaction_date__lte=self.report_date)
            total_returns = 0
            for payment in filtered_returns:
                total_returns += payment.amount
            self.remaining_loan = self.total_loan - total_returns
        super().save(*args, **kwargs)
