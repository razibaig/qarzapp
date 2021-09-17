from django.db import models
from django.db.models import Q
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify

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
    unique_id = AutoSlugField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(QarzUser, self).save()
        if not self.unique_id:  # if this is a new user
            unique_slug = '{0}{1}'.format(str(self.type)[0], str(self.pk))
            self.unique_id = slugify(unique_slug)
            self.save()


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
    total_donated = models.IntegerField(blank=True, null=True, default=0)
    total_loan = models.IntegerField(blank=True, null=True, default=0)
    remaining_loan = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.report_user.name

    def save(self, *args, **kwargs):
        user_transactions = Transaction.objects.filter(qarz_user=self.report_user).filter(type=DONATION)
        filtered_donations = user_transactions.filter(transaction_date__lte=self.report_date)
        total_donations = 0
        for donation in filtered_donations:
            total_donations += donation.amount
        # set the total_donated field
        self.total_donated = total_donations

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


class OverallReport(models.Model):
    report_date = models.DateTimeField(null=True, blank=True)
    total_donations = models.IntegerField(blank=True, null=True, default=0)
    total_loans = models.IntegerField(blank=True, null=True, default=0)
    current_balance = models.IntegerField(blank=True, null=True, default=0)
    outstanding_loans = models.IntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        donations = Transaction.objects.filter(type=DONATION).filter(transaction_date__lte=self.report_date)
        returns = Transaction.objects.filter(type=RETURN).filter(transaction_date__lte=self.report_date)
        loans = Transaction.objects.filter(type=LOAN).filter(transaction_date__lte=self.report_date)
        td = sum([donation.amount for donation in donations])
        tr = sum([ret.amount for ret in returns])
        tl = sum([loan.amount for loan in loans])
        tb = td + tr - tl
        ol = tl - tr
        self.total_donations = td
        self.total_loans = tl
        self.current_balance = tb
        self.outstanding_loans = ol
        super().save(*args, **kwargs)
