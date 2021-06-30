from django.contrib import admin
from .models import QarzUser, Transaction, Report, OverallReport


class UserAdmin(admin.ModelAdmin):
    list_display = ('cnic', 'name', 'mobile', 'type')
    search_fields = ['cnic', 'name', 'mobile', 'type']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('qarz_user', 'transaction_date', 'amount', 'type')


class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.get_fields()]
    exclude = ('total_donated', 'total_loan', 'remaining_loan')


class OverallReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OverallReport._meta.get_fields()]
    exclude = ('total_donations', 'total_loans', 'current_balance', 'outstanding_loans')


admin.site.register(QarzUser, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(OverallReport, OverallReportAdmin)
