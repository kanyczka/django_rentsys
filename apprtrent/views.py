from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

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


class AddAppartment(CreateView):

    model = Appartment
    fields = '__all__'
    template_name_suffix = '_create_form'       # zmienia nazwę szablonu z appartment_form na appartment_create_form
    success_url = reverse_lazy('display')
    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse('add-photo', args=[self.object.id])
        return super().form_valid(form)


class AddAppartmentsPhoto(View):

    def get(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        form = AddAppartmentPhotoForm(instance=appartment)

        return render(request, "apprtrent/display.html", {"form": form, "button": "Dodaj zdjęcie"})

    def post(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        form = AddAppartmentPhotoForm(request.POST, request.FILES, instance=appartment)
        if form.is_valid():
            form.save()
            return redirect(reverse('add-photo', args=[appartment_id]))
        else:
            return render(request, "apprtrent/display.html", {"form": form, "button": "Dodaj zdjęcie"})





