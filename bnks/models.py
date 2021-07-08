from django.contrib.auth.models import AbstractUser, User
from django.db import models
from WeGoTripProject import settings
from bnks.validator import validate_none


class Client(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(blank=False, null=False, verbose_name='Эл. почта', validators=[validate_none])
    full_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Полное имя',
                                 validators=[validate_none])
    phone = models.CharField(max_length=16, blank=True, verbose_name='Телефон')
    reward = models.FloatField(default=0, verbose_name='Вознаграждеине')

    def __str__(self):
        return f'Пользователь - {self.full_name}'


class Payment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор платежа', on_delete=models.CASCADE,
                               blank=False, validators=[validate_none])
    amount_of_payment = models.FloatField(verbose_name='Сумма платежа')
    date_of_payment = models.DateTimeField(verbose_name='Время платежа')

    def __str__(self):
        return f'Платеж {self.id}, автор платежа {self.author.full_name}'


class Payback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор платежа', on_delete=models.CASCADE,
                             blank=False, validators=[validate_none])
    amount_of_payback = models.FloatField(verbose_name='Сумма выплаты', blank=False, validators=[validate_none])
    date_of_creating = models.DateTimeField(verbose_name='Дата создания заявки')
    date_of_work = models.DateTimeField(null=True, blank=True, verbose_name='Дата обработки')
    is_payed = models.BooleanField(blank=False, default=False, verbose_name='Провели ли выплату')
    account_number = models.CharField(max_length=20, verbose_name='Номер счета', blank=True)

    def __str__(self):
        return f'Выплата {self.id}, автор платежа {self.user.full_name}'
