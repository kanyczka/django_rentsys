from django import forms
from django.core.validators import EmailValidator, URLValidator
from apprtrent.models import Photo, User, Appartment

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

