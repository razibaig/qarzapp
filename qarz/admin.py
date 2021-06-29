from django.contrib import admin
from .models import QarzUser, Transaction, Report


class UserAdmin(admin.ModelAdmin):
    list_display = ('cnic', 'name', 'mobile', 'type')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('qarz_user', 'transaction_date', 'amount', 'donation_or_loan')


class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.get_fields()]


admin.site.register(QarzUser, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Report, ReportAdmin)
