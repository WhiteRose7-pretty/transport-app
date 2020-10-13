from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
    company = models.BooleanField(default=False)

    def __str__(self):
        return self.email



class UserHelpedElement(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Właściciel')
    basic = models.BooleanField(default=False)
    verified = models.BooleanField(verbose_name='Konto zweryfikowane', default=False)
    type_account = models.CharField(max_length=50, verbose_name='Typ konta', default='Standard')
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    money = models.DecimalField(max_digits=20, decimal_places=2, default=0)


    class Meta:
        verbose_name = 'Dodatkowe infomacje o koncie'
        verbose_name_plural = 'Dodatkowe infomacje o koncie'



class CompanyUserData(models.Model):
    PROVINCES_CHOICES = [
        ('Mazowieckie', 'Mazowieckie'),
        ('Śląskie', 'Śląskie'),
        ('Wielkopolskie', 'Wielkopolskie'),
        ('Małopolskie', 'Małopolskie'),
        ('Dolnośląskie', 'Dolnośląskie'),
        ('Łódzkie', 'Łódzkie'),
        ('Pomorskie', 'Pomorskie'),
        ('Podkarpackie', 'Podkarpackie'),
        ('Lubelskie', 'Lubelskie'),
        ('Kujawsko-pomorskie', 'Kujawsko-pomorskie'),
        ('Zachodniopomorskie', 'Zachodniopomorskie'),
        ('Warmińsko-mazurskie', 'Warmińsko-mazurskie'),
        ('Świętokrzyskie', 'Świętokrzyskie'),
        ('Podlaskie', 'Podlaskie'),
        ('Lubuskie', 'Lubuskie'),
        ('Opolskie', 'Opolskie'),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Właściciel')
    company_name = models.CharField(max_length=500)
    nip = models.CharField(max_length=20)
    province = models.CharField(max_length=50, choices=PROVINCES_CHOICES)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    street = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Dane użytkownika do faktury'
        verbose_name_plural = 'Dane użytkownika do faktury'
