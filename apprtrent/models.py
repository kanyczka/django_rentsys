from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = 'użytkownik'
        verbose_name_plural = 'użytkownicy'
        ordering = ['username']


class Owner(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Imię", null=True)
    last_name = models.CharField(max_length=64, verbose_name="Nazwisko", null=True)
    company_name = models.CharField(max_length=128, verbose_name="Nazwa firmy", null=True)
    if_vat = models.BooleanField(default=True, verbose_name="płatnik VAT", help_text='Czy jest płatnikiem VAT')
    vat_number = models.CharField(max_length=10, null=True, verbose_name="NIP")
    address_city = models.CharField(max_length=128, verbose_name="Miasto")
    address_code = models.CharField(max_length=6, help_text="00-000", verbose_name="kod")
    address_str = models.CharField(max_length=128, verbose_name="Ulica i nr")
    address_no = models.CharField(max_length=16, null=True, verbose_name="nr lokalu")
    tel_no = models.CharField(max_length=32, null=True, verbose_name="Nr telefonu")
    e_mail = models.EmailField(null=True, verbose_name="Email")
    comment = models.TextField(null=True, blank=True, verbose_name="Dodatkowe informacje")

    class Meta:
        verbose_name = 'Właścicel'
        verbose_name_plural = 'Właściciele'

    def __str__(self):
        return self.first_name + self.last_name + self.company_name


APP_FACILITIES = (
    (1, "wifi"),
    (2, "TV kablowa"),
    (3, "TV"),
    (4, "winda"),
    (4, "wyposażona kuchnia"),
    (5, "zestaw do parzenia kawy"),
    (6, "żelazko"),
    (7, "suszarka"),
    (8, "pralka"),
    (9, "taras/balkon"),
    (10, "klimatyzacja"),
    (11, "prysznic"),
    (12, "wanna"),
    (13, "piekarnik"),
    (14, "mikrofalówka"),
    (15, "kominek"),
)

DEPOSIT_VALUES = (
    (1, "100"),
    (2, "200"),
    (3, "300"),
    (4, "400"),
    (5, "500"),
    (6, "600"),
)


class Fee(models.Model):
    name = models.CharField(max_length=64, verbose_name="dodatkowa opłata")
    fee_value = models.DecimalField(max_digits=6, decimal_places=2)

class City(models.Model):
    city_name = models.CharField(max_length=60, verbose_name="miasto")


class Appartment(models.Model):
    app_name = models.CharField(max_length=128, verbose_name="Nazwa apartamentu")
    description = models.TextField(verbose_name="Opis apartamentu")
    address_city = models.ForeignKey(City, on_delete=models.CASCADE)
    address_code = models.CharField(max_length=6, help_text="00-000", verbose_name="kod")
    address_str = models.CharField(max_length=128, verbose_name="Ulica i nr")
    address_no = models.CharField(max_length=16, null=True, verbose_name="nr lokalu")
    area = models.SmallIntegerField(verbose_name="powierzchnia")
    floor = models.SmallIntegerField(verbose_name="piętro")
    no_of_rooms = models.SmallIntegerField(verbose_name="liczba pokoi")
    no_of_guests = models.SmallIntegerField(verbose_name="liczba osób")
    no_of_beds = models.SmallIntegerField(verbose_name="liczba łóżek")
    own_parking = models.BooleanField(default=False, verbose_name="miejsce parkingowe")
    facilities = models.SmallIntegerField(choices=APP_FACILITIES, verbose_name="Udogodnienia/Wyposażenie")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit = models.SmallIntegerField(choices=DEPOSIT_VALUES, verbose_name="zwrotna kaucja")
    fees = models.ForeignKey(Fee, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    best_app = models.BooleanField(default=True)

    class Meta:
        ordering = ['address_city', 'price']

    def __str__(self):
        return self.app_name

class Photo(models.Model):
    path = models.ImageField(max_length=128, upload_to="photos/", verbose_name="zdjęcie apartamentu")
    appartment = models.ForeignKey(Appartment, on_delete=models.CASCADE)


class Booking(models.Model):
    checkin_date = models.DateTimeField(verbose_name="Rezerwacja od dnia")
    checkout_date = models.DateTimeField(verbose_name="Rezerwacja do dnia")
    appartment = models.ForeignKey(Appartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('checkin_date', 'checkout_date', 'appartment')

    def __str__(self):
        return f'{self.appartment}, {self.checkin_date}, {self.checkout_date}, {self.user}'


class Article(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nazwa artykułu")
    article_text = models.TextField(null=True, blank=True)



