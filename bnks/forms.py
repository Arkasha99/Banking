from django import forms

from bnks.models import Payment, Payback


class CreatePayment(forms.ModelForm):
    amount_of_payment = forms.FloatField(label='Сумма платежа', required=True)

    class Meta:
        model = Payment
        fields = ['amount_of_payment']


class CreatePayback(forms.ModelForm):
    amount_of_payback = forms.FloatField(label='Сумма выплаты', required=True)
    account_number = forms.CharField(label='Номер счета', max_length=30, required=False)

    class Meta:
        model = Payback
        fields = ['amount_of_payback', 'account_number']
