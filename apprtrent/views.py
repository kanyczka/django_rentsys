from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from apprtrent.models import Appartment


# Home
class HomeView(View):

    def get(self,request):
        appartments = Appartment.objects.filter(best_app=True).order_by("price")
        return render(request, "RentSystem/index.html", {"appartments": appartments})

# Tworzenie nowego usera
class SingUP(View):

        def post(self, request):
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            else:
                form = UserCreationForm()
            return render(request, 'RentSystem/signup.html', {'form': form})


# Logowanie i wylogowywanie
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "photoalbum/display.html", {"form": form, "button": "Zaloguj się"})


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password) # zwraca Nona jeżeli podaliśmy złe dane
            if user is None:
                form.add_error('username',
                               'Login lub hasło jest niepoprawne')
                return render(request, "photoalbum/index.html",
                              {"form": form,
                               "button": "Zaloguj się"})
            login(request, user)
            return redirect(reverse('index'))

# todo utworzyć dodawanie app i zdjęć do nich
# w indexe są odnośniki do linków, gdzie jest położenie plików



