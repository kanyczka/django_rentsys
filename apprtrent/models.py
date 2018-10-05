from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


DISTANCE = (
    (1, "bardzo blisko"),
    (2, "blisko"),
    (3, "dojazd komunikacją miejską"),
    (4, "dłuższy dojazd komunikacją miejską"),
)



class User(AbstractUser):
    class Meta:
        verbose_name = 'użytkownik'
        verbose_name_plural = 'użytkownicy'
        ordering = ['username']


class Owner(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Imię", blank=True)
    last_name = models.CharField(max_length=64, verbose_name="Nazwisko", blank=True)
    company_name = models.CharField(max_length=128, verbose_name="Nazwa firmy", blank=True)
    if_vat = models.BooleanField(default=True, verbose_name="płatnik VAT", help_text='Czy jest płatnikiem VAT')
    vat_number = models.CharField(max_length=10, blank=True, verbose_name="NIP")
    address_city = models.CharField(max_length=128, verbose_name="Miasto")
    address_code = models.CharField(max_length=6, help_text="00-000", verbose_name="kod")
    address_str = models.CharField(max_length=128, verbose_name="Ulica i nr")
    address_no = models.CharField(max_length=16, blank=True, verbose_name="nr lokalu")
    tel_no = models.CharField(max_length=32, verbose_name="Nr telefonu", blank=True)
    e_mail = models.EmailField(blank=True, verbose_name="Email")
    comment = models.TextField(blank=True, verbose_name="Dodatkowe informacje")

    class Meta:
        verbose_name = 'Właścicel'
        verbose_name_plural = 'Właściciele'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.company_name}'


class City(models.Model):
    city_name = models.CharField(max_length=60, verbose_name="miasto")

    def __str__(self):
        return self.city_name

class Facility(models.Model):
    name = models.CharField(max_length=64, verbose_name="Udogodnienia/Wyposażenie")

    def __str__(self):
        return self.name

class Fee(models.Model):
    name = models.CharField(max_length=64, verbose_name="dodatkowa opłata")
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name



class Appartment(models.Model):
    app_name = models.CharField(max_length=128, verbose_name="Nazwa apartamentu")
    description = models.TextField(verbose_name="Opis apartamentu", blank=True)
    address_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="miasto")
    address_code = models.CharField(max_length=6, help_text="00-000", verbose_name="kod")
    address_str = models.CharField(max_length=128, verbose_name="Ulica i nr")
    address_no = models.CharField(max_length=16, blank=True, verbose_name="nr lokalu")
    area = models.SmallIntegerField(verbose_name="powierzchnia")
    floor = models.SmallIntegerField(verbose_name="piętro")
    no_of_rooms = models.SmallIntegerField(verbose_name="liczba pokoi")
    no_of_guests = models.SmallIntegerField(verbose_name="liczba osób")
    no_of_beds = models.SmallIntegerField(verbose_name="liczba łóżek")
    facilities = models.ManyToManyField(Facility, verbose_name="udogodnienia/wyposażenie")
    fees = models.ManyToManyField(Fee, verbose_name="dodatkowe opłaty")
    day_price = models.DecimalField(max_digits=6, default=200.00, decimal_places=2, verbose_name="Cena za dzień")
    coders_weekly_price = models.DecimalField(max_digits=6, default=400.00, decimal_places=2, blank=True, null=True, verbose_name="Cena tygodniowego wynajmu dla kursantów Coderslab")
    deposit = models.SmallIntegerField(default=0, verbose_name="zwrotna kaucja")
    best_app = models.BooleanField(default=True, verbose_name="wyróżniony", help_text="czy apartament ma być pokazywany na stronie głównej")
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="właściciel")
    distance = models.SmallIntegerField(choices=DISTANCE, verbose_name="odległość od Coderslab")


    class Meta:
        ordering = ['address_city', 'app_name']
        permissions = (
            ("new_appartment", "Can add new appartment"),
            # ("change_appartment", "Can change appartment"),
            # ("delete_appartment", "Can delete appartment"),

            )

    def __str__(self):
        return self.app_name


def app_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/app_<id>/<filename>
    return 'app_{0}/{1}'.format(instance.appartment.id, filename)


class Photo(models.Model):
    # path = models.ImageField(max_length=128, upload_to="photos/", verbose_name="zdjęcie apartamentu")
    path = models.ImageField(max_length=128, upload_to=app_directory_path, verbose_name="zdjęcie apartamentu")
    appartment = models.ForeignKey(Appartment, on_delete=models.CASCADE)


class Booking(models.Model):
    checkin_date = models.DateField(default=date.today, blank=True, verbose_name="Rezerwacja od dnia")
    checkout_date = models.DateField(verbose_name="Rezerwacja do dnia")
    appartment = models.ForeignKey(Appartment, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        unique_together = ('checkin_date', 'checkout_date', 'appartment')

    def __str__(self):
        return f'{self.appartment}, {self.checkin_date}, {self.checkout_date}'


class Article(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nazwa artykułu")
    article_text = models.TextField(blank=True)

    def __str__(self):
        return self.name



