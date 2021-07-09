import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

# Create your views here.
from django.views import generic

from bnks.forms import CreatePayment, CreatePayback, SignUpForm
from bnks.models import Client, Payment

User = get_user_model()
current_timezone = timezone.get_current_timezone()


class RegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


def index(request):
    form = CreatePayment()
    return render(request, 'index.html', {'form': form})


# Создание объекта платежа
def create_payment(request):
    if request.method == 'POST':
        form = CreatePayment(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.author = request.user
            payment.amount_of_payment = float(form.cleaned_data['amount_of_payment'])
            payment.date_of_payment = datetime.datetime.now(tz=current_timezone)
            payment.save()
            request.user.reward = request.user.reward + float(form.cleaned_data['amount_of_payment']) * 0.3
            request.user.save()
            return redirect('index')
        else:
            error = form.errors
            return redirect('index', {'error': error})


# Личный профиль пользователя с заказом выплаты
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
            payback.date_of_creating = datetime.datetime.now(tz=current_timezone)
            payback.is_payed = False
            if form.cleaned_data['account_number'] != '':
                payback.account_number = form.cleaned_data['account_number']
            payback.save()
    form = CreatePayback()
    return render(request, 'profile.html', {'user': user, 'form': form})


# Создание платежа через консоль
def create_payment_console(user_id, payment):
    user = Client.objects.filter(id=user_id).get()
    payment_obj = Payment.objects.create(author=user, amount_of_payment=float(payment),
                                         date_of_payment=datetime.datetime.now(tz=current_timezone))
    print(type(payment))
    user.reward += float(payment)
    payment_obj.save()
    user.save()
    return 'Payment created succesfully'
