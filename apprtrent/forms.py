from django import forms
from django.core.validators import EmailValidator, URLValidator
from apprtrent.models import Photo, User

from django.contrib.auth import forms as forms2



class UserCreationForm2(forms2.UserCreationForm):
   class Meta(forms2.UserCreationForm.Meta):
       model = User


class AddAppartmentPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('path',)



