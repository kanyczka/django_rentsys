from django import forms
from django.core.validators import EmailValidator, URLValidator
from apprtrent.models import Photo, User, Appartment, Owner, Booking, City

from django.contrib.auth import forms as forms2


class UserCreationForm2(forms2.UserCreationForm):
    class Meta(forms2.UserCreationForm.Meta):
        model = User


class AddAppartmentPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('path',)
        labels = {
            'path': "Nowe zdjęcie"
        }


class AddAppartmentForm(forms.ModelForm):
    class Meta:
        model = Appartment
        fields = '__all__'
        widgets = {
            'facilities': forms.CheckboxSelectMultiple,
            'fees': forms.CheckboxSelectMultiple,
        }


class SearchAppartmentsInCity(forms.ModelForm):
    class Meta:
        model = Appartment
        fields = ('address_city',)
        labels = {
            'address_city': 'Wybierz miasto ',
        }


class SearchAppartmentsInCityCodersLabDist(forms.ModelForm):
    class Meta:
        model = Appartment
        fields = ('distance', 'address_city',)
        widgets = {
            'address_city': forms.HiddenInput
        }


class AddOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'


class AddBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('checkin_date', 'checkout_date', 'email')
        widgets = {
            'checkin_date': forms.TextInput(attrs={'type': 'date'}),
            'checkout_date': forms.TextInput(attrs={'type': 'date'}),
        }
        labels = {
            'checkin_date': "Najbliższy wolny termin"
        }

    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        # if not checkin_date:
        #     msg = "Podaj prawidłową datę"
        #     self.add_error('checkin_date', msg)
        # if not checkout_date:
        #     msg = "Podaj prawidłową datę"
        #     self.add_error('checkout_date', msg)

        if checkin_date >= checkout_date:
            raise forms.ValidationError(
                "Data powinna być poźniejesza niż data początku rezerwacji"
            )
        return cleaned_data
