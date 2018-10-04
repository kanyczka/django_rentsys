from django import forms
from django.core.validators import EmailValidator, URLValidator
from apprtrent.models import Photo, User, Appartment, Owner, Booking

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


class AddOwnerForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = '__all__'


class AddBookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('checkin_date', 'checkout_date',)

