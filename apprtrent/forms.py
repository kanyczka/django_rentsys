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


class AddAppartmentForm(forms.ModelForm):

    class Meta:
        model = Appartment
        fields = '__all__'
        widgets = {
            'facilities': forms.CheckboxSelectMultiple,
            'fees': forms.CheckboxSelectMultiple,
        }

class SearchAppatmentsInCity(forms.ModelForm):

    class Meta:
        model = Appartment
        fields = ('address_city',)
        labels = {
            'address_city': 'Wybierz miasto ',
        }




class AddOwnerForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = '__all__'


class AddBookingForm(forms.ModelForm):

    # checkin_date = forms.DateField()
    # checkout_date = forms.DateField()


    class Meta:
        model = Booking
        fields = ('checkin_date', 'checkout_date', 'email',)

    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        if checkin_date >= checkout_date:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                "Data powinna być poźniejesza niż data początku rezerwacji"
                )
        return cleaned_data