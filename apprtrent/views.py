from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apprtrent.forms import AddAppartmentPhotoForm, UserCreationForm2
from apprtrent.models import Appartment


# Home
class HomeView(View):

    def get(self,request):
        appartments = Appartment.objects.filter(best_app=True).order_by("price")
        return render(request, "apprtrent/home.html")
        # return render(request, "apprtrent/home.html", {"appartments": appartments})

# Tworzenie nowego usera
class SignUPView(View):

        def post(self, request):
            form = UserCreationForm2(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            return render(request, 'apprtrent/signup.html', {'form': form})
        def get(self, request):
            form = UserCreationForm()
            return render(request, 'apprtrent/signup.html', {'form': form})



# todo utworzyć dodawanie app i zdjęć do nich
# w indexe są odnośniki do linków, gdzie jest położenie plików


class AddAppartment(View):
    def get(self, request):
        form = AddPhotoForm()
        return render(request, "photoalbum/display.html", {"form": form,
                                                           "button": "Dodaj fotkę"})

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
        else:
            return render(request, "photoalbum/display.html", {"form": form,
                                                                   "button": "Dodaj fotkę"})


class AddAppartmentsPhoto(View):

    def get(self, request):
        form = AddAppartmentPhotoForm()
        return render(request, "apprtrent/display.html", {"form": form,
                                                           "button": "Dodaj zdjęcie"})
    def post(self, request):
        form = AddAppartmentPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            return render(request, "apprtrent/display.html", {"form": form, "button": "Dodaj zdjęcie"})




