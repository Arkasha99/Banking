import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from bnks.forms import CreatePayment, CreatePayback

User = get_user_model()


def index(request):
    form = CreatePayment()
    return render(request, 'index.html', {'form': form})


def create_payment(request):
    if request.method == 'POST':
        form = CreatePayment(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.author = request.user
            payment.amount_of_payment = float(form.cleaned_data['amount_of_payment'])
            payment.date_of_payment = datetime.datetime.now()
            payment.save()
            request.user.reward = request.user.reward + float(form.cleaned_data['amount_of_payment'])*0.3
            request.user.save()
            return redirect('index')
        else:
            error = form.errors
            return redirect('index', {'error': error})


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = CreatePayback(request.POST)
        if form.is_valid():
            payback = form.save(commit=False)
            payback.user = request.user
            if request.user.reward >= float(form.cleaned_data['amount_of_payback']):
                payback.amount_of_payback = float(form.cleaned_data['amount_of_payback'])
            else:
                error = 'Баланс на вашем счету меньше запрашиваемой суммы, попробуйте чуть меньше'
                form = CreatePayback()
                return render(request, 'profile.html', {'user': user, 'error': error, 'form': form})
            payback.date_of_creating = datetime.datetime.now()
            payback.is_payed = False
            if form.cleaned_data['account_number'] != '':
                payback.account_number = form.cleaned_data['account_number']
            payback.save()
    form = CreatePayback()
    return render(request, 'profile.html', {'user': user, 'form': form})

