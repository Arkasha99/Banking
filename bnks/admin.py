import datetime
import json

import requests
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.utils import timezone

from bnks.models import Client, Payment, Payback

# Register your models here.
admin.site.register(Client)
admin.site.register(Payment)


@admin.register(Payback)
class PaybackAdmin(admin.ModelAdmin):
    fields = ('user', 'amount_of_payback', 'is_payed', 'date_of_creating', 'date_of_work', 'account_number')
    list_display = ('user', 'amount_of_payback', 'is_payed',)
    change_form_template = 'admin/account/account_action.html'

    def get_readonly_fields(self, request, obj=None):
        if obj.is_payed:
            return ('user', 'amount_of_payback','date_of_creating', 'is_payed' ,'date_of_work', 'account_number')
        else:
            return super(PaybackAdmin, self).get_readonly_fields(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('payback/<int:pk>', self.admin_site.admin_view(self.make_payback), name='admin_payback')
        ]
        return urls+custom_urls

    def make_payback(self, request, pk):
        payback_obj = Payback.objects.get(id=pk)
        payback_obj.date_of_work = datetime.datetime.now(tz=timezone.get_current_timezone())
        payback_obj.is_payed = True
        if payback_obj.user.reward >= payback_obj.amount_of_payback:
            payback_obj.user.reward -= payback_obj.amount_of_payback
        else:
            raise ValueError('На счету недостаточно денег!')
        payback_obj.user.save()
        payback_obj.save()
        if payback_obj.account_number:
            payload = {"account": payback_obj.account_number, "amount": payback_obj.amount_of_payback}
            r = requests.post('https://webhook.site/014a8aad-7e72-4059-9e36-60eac173c40b', data=json.dumps(payload))
        return redirect('admin:index')
