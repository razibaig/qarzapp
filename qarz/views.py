from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import QarzUser, Transaction, DONOR, LOANER, DONATION, LOAN, RETURN


# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


class SystemReport(TemplateView):
    template_name = 'admin/system_report/system_report.html'

    @staticmethod
    def calculate_user_stats(user_list):
        user_data_dict = {}
        for user_obj in user_list:
            total_donated, total_loan, remaining_loan = 0, 0, 0
            user_transactions = Transaction.objects.filter(qarz_user=user_obj).filter(type=DONATION)
            total_donations = 0
            for donation in user_transactions:
                total_donations += donation.amount
            # calculate the total_donated
            total_donated = total_donations

            user_loans = Transaction.objects.filter(qarz_user=user_obj).filter(type=LOAN)
            total_loans = 0
            for loan in user_loans:
                total_loans += loan.amount
            # calculate the total_loan
            total_loan = total_loans

            user_returns = Transaction.objects.filter(qarz_user=user_obj).filter(type=RETURN)
            total_returns = 0
            for payment in user_returns:
                total_returns += payment.amount
            remaining_loan = total_loan - total_returns
            # add the user data to dictionary
            user_data_dict.update({user_obj.id: {"total_donated": total_donated, "total_loan": total_loan, "remaining_loan": remaining_loan}})
        return user_data_dict

    @staticmethod
    def calculate_system_stats():
        donations = Transaction.objects.filter(type=DONATION)
        returns = Transaction.objects.filter(type=RETURN)
        loans = Transaction.objects.filter(type=LOAN)
        td = sum([donation.amount for donation in donations])
        tr = sum([ret.amount for ret in returns])
        tl = sum([loan.amount for loan in loans])
        tb = td + tr - tl
        ol = tl - tr
        total_donations = td
        total_loans = tl
        current_balance = tb
        outstanding_loans = ol
        return {"t_d": total_donations, "t_l": total_loans, "c_b": current_balance, "o_l": outstanding_loans}

    def get(self, request, *args, **kwargs):
        context = {}
        users = QarzUser.objects.all()
        user_stats = self.calculate_user_stats(users)
        users_list = []
        for user in users:
            user_dict = {"name": user.name, "type": user.type, "t_d": user_stats[user.id]['total_donated'],
                         "t_l": user_stats[user.id]['total_loan'], "r_l": user_stats[user.id]['remaining_loan']}
            users_list.append(user_dict)
        context['users'] = users_list
        context['system_data'] = self.calculate_system_stats()

        return render(request, self.template_name, context)
