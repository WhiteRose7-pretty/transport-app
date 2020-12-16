from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

from authentication.models import CustomUser
from .choices import PROVINCES_CHOICES
from ckeditor.fields import RichTextField
from .choices import P24_STATUS_CHOICES


class Przelewy24Transaction(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    status = models.IntegerField(choices=P24_STATUS_CHOICES)
    order_id_full = models.CharField(max_length=100, null=True, blank=True)
    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class TypeProduct(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nazwa typu produktu')
    icons = models.ImageField(verbose_name='Zdjęcie', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Typy produktów'
        verbose_name_plural = 'Typy produktów'


class NewOrder(models.Model):
    type_product = models.CharField(max_length=500)
    location_name_from = models.CharField(max_length=500, verbose_name='Lokalizacja nadawcy')
    org_latitude_form = models.CharField(max_length=500, verbose_name='Współrzedne nadawcy (Szerokość geograficzna)')
    org_longitude_from = models.CharField(max_length=500, verbose_name='Współrzedne nadawcy (Długość geograficzna)')
    location_name_to = models.CharField(max_length=500, verbose_name='Lokalizacja odbiorcy')
    org_latitude_to = models.CharField(max_length=500, verbose_name='Współrzedne odbiorcy (Szerokość geograficzna)')
    org_longitude_to = models.CharField(max_length=500, verbose_name='Współrzedne odbiorcy (Długość geograficzna)')
    distance = models.CharField(max_length=500, verbose_name='Odległość między punktami')
    # date_st_send = models.CharField(max_length=50, verbose_name='Data wysłania paczki od')
    # date_end_send = models.CharField(max_length=50, verbose_name='Data wysłania paczki do', blank=True)
    # date_st_received = models.CharField(max_length=50, verbose_name='Data wysłania paczki do', blank=True)
    # date_end_received = models.CharField(max_length=50, verbose_name='Data wysłania paczki do', blank=True)
    date_st_send = models.DateTimeField( verbose_name='Data wysłania paczki od')
    date_end_send = models.DateTimeField(verbose_name='Data wysłania paczki do', blank=True, null=True)
    date_st_received = models.DateTimeField(verbose_name='Data wysłania paczki do', blank=True, null=True)
    date_end_received = models.DateTimeField(verbose_name='Data wysłania paczki do', blank=True, null=True)
    image_1 = ProcessedImageField(upload_to='profile-pictures',
                                  verbose_name='Zdjęcie poglądowe 1',
                                  processors=[ResizeToFit(1080, 1080)],
                                  format='JPEG',
                                  options={'quality': 100},
                                  blank=True, null=True)
    profile_pictures = ImageSpecField(source='image_1',
                                      processors=[ResizeToFill(400, 400)],
                                      format='JPEG',
                                      options={'quality': 80})
    image_2 = ProcessedImageField(upload_to='profile-pictures',
                                  verbose_name='Zdjęcie poglądowe 2',
                                  processors=[ResizeToFit(1080, 1080)],
                                  format='JPEG',
                                  options={'quality': 100},
                                  blank=True, null=True)
    image_3 = ProcessedImageField(upload_to='profile-pictures',
                                  verbose_name='Zdjęcie poglądowe 3',
                                  processors=[ResizeToFit(1080, 1080)],
                                  format='JPEG',
                                  options={'quality': 100},
                                  blank=True, null=True)
    items_descriptions = models.TextField(verbose_name='Opis przedmiotu', blank=True)
    width = models.IntegerField(verbose_name='Szerokość paczki')
    depth = models.IntegerField(verbose_name='Długość paczki')
    height = models.IntegerField(verbose_name='Wysokość paczki')
    weight = models.IntegerField(verbose_name='Waga paczki')
    quantity = models.IntegerField(verbose_name='Ilość sztuk do przesłania')
    email = models.EmailField(verbose_name='Adres email')
    phone = models.CharField(max_length=30, verbose_name='Numer telefonu')
    contact_person = models.CharField(max_length=50)
    unique_url = models.URLField(verbose_name='URL przesyłki', blank=True)
    custom_id = models.CharField(max_length=500, blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Cena', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data edycji')
    transaction = models.ForeignKey(Przelewy24Transaction, on_delete=models.CASCADE, null=True, blank=True, related_name='order')

    def __str__(self):
        return '%s - %s' % (self.type_product, self.pk)

    def verified(self):
        if self.transaction:
            if self.transaction.status == 3:
                return True
        return False

    class Meta:
        verbose_name = 'Wyceny'
        verbose_name_plural = 'Wyceny'


class CompanyUser(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Właściciel', blank=True, null=True)
    company_name = models.CharField(max_length=500, verbose_name='Nazwa firmy')
    company_phone = models.CharField(max_length=30, verbose_name='Telefon kontaktowy')
    company_email = models.EmailField(verbose_name='Adres email')
    nip = models.CharField(max_length=20, verbose_name='NIP')
    location = models.CharField(max_length=500)
    blocked = models.BooleanField(default=False)
    licence = models.FileField(verbose_name='Licencja', blank=True, null=True)
    contact_person = models.CharField(max_length=50, verbose_name='Osoba kontaktowa')
    directions_supported = models.CharField(max_length=500)
    vehicle_fleet = models.TextField()

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Firmy'
        verbose_name_plural = 'Firmy'


class OfferResponse(models.Model):
    owner = models.ForeignKey(NewOrder, on_delete=models.CASCADE, verbose_name='Właściciel')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, verbose_name='Firma')
    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Cena')
    date = models.DateTimeField(verbose_name='Data')
    comments = models.TextField(verbose_name='Komentarz')
    displayed = models.BooleanField(default=True, verbose_name='Pokaż oferte')

    class Meta:
        verbose_name = 'Odpowiedzi na oferty'
        verbose_name_plural = 'Odpowiedzi na oferty'


class Payment(models.Model):
    owner = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, verbose_name='Własciciel')
    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Cena')
    package = models.CharField(max_length=50, verbose_name='Pakiet')
    status = models.CharField(max_length=50, verbose_name='Status płatności')

    class Meta:
        verbose_name = 'Płatności i statusy'
        verbose_name_plural = 'Płatności i statusy'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nazwa kategorii')
    displayed_in_navbar = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorie'


class Newsletter(models.Model):
    topic = models.CharField(max_length=50, verbose_name='Temat postu')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoria')
    sub_title = models.TextField()
    bg_img = ProcessedImageField(upload_to='profile-pictures',
                                 processors=[ResizeToFill(1920, 1080)],
                                 format='JPEG',
                                 options={'quality': 100})
    img = ProcessedImageField(upload_to='profile-pictures',
                              verbose_name='Zdjęcie artykułu',
                              processors=[ResizeToFit(1920, 1920)],
                              format='JPEG',
                              options={'quality': 100})
    img_800x600 = ImageSpecField(source='img',
                                 processors=[ResizeToFill(800, 600)],
                                 format='JPEG',
                                 options={'quality': 80})
    content = RichTextField(verbose_name='Treść postu')
    owner = models.CharField(max_length=75, verbose_name='Autor postu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data edycji')

    class Meta:
        verbose_name = 'NewsLetter/Blog - artykuły'
        verbose_name_plural = 'NewsLetter/Blog - artykuły'
        ordering = ['-created_at']


class Coments(models.Model):
    owner = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='Post')
    user_name = models.CharField(max_length=50, verbose_name='Nazwa użytkownika')
    content = models.CharField(max_length=50, verbose_name='Treść komentarza')
    displayed = models.BooleanField(verbose_name='Pokaż komentarz')

    class Meta:
        verbose_name = 'Komentarze'
        verbose_name_plural = 'Komentarze'


class ChangeLog(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    change = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = 'Logi zmian'
        verbose_name_plural = 'Logi zmian'


class Chat(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = 'Instancje czatu'
        verbose_name_plural = 'Instancje czatu'


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()


class AdditionalOrderDetails(models.Model):
    owner = models.ForeignKey(NewOrder, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=50)
    sender = models.CharField(max_length=50)
    comments = models.TextField()

    class Meta:
        verbose_name = 'Dodatkowe szczegóły zamówień'
        verbose_name_plural = 'Dodatkowe szczegóły zamówień'


class Parametrs(models.Model):
    id_obj = models.IntegerField()
    par_name = models.CharField(max_length=200)
    par_value = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    par_active = models.CharField(max_length=200)

