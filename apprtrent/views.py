from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from apprtrent.forms import AddAppartmentPhotoForm, UserCreationForm2, AddAppartmentForm
from apprtrent.models import Appartment, Photo, Facility, Owner, City


# Home
class HomeView(View):

    def get(self,request):
        return redirect(reverse('appartments'))

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


# class AddAppartment(CreateView):
#
#     model = Appartment
#     fields = '__all__'
#     template_name_suffix = '_create_form'       # zmienia nazwę szablonu z appartment_form na appartment_create_form
#     success_url = reverse_lazy('display')
#
#     def form_valid(self, form):
#         self.object = form.save()
#         self.success_url = reverse('add-photo', args=[self.object.id])
#         return super().form_valid(form)


# lista apartamentów do edycji
class AppartmentsEditList(View):
    def get(self, request):
        appartments = Appartment.objects.all().order_by("address_city", "price")
        photos = Photo.objects.all()
        return render(request, "apprtrent/appartment_edit_list.html", {"appartments": appartments, "photos": photos})


# dodawanie apartamentu z ograniczonymi uprawnieniami
class AddAppartment(PermissionRequiredMixin, View):
    permission_required = 'apprtrent.new_appartment'

    def get(self, request):
        form = AddAppartmentForm()
        return render(request, "apprtrent/appartment_create_form.html", {"form": form})
    def post(self, request):
        form = AddAppartmentForm(request.POST)
        if form.is_valid():
            appartment = form.save()
            return redirect(reverse('add-photo', args=[appartment.id]))
        return render(request, "apprtrent/appartment_create_form.html", {"form": form})


# edycja i zmiana danych w apartamentcie
class ChangeAppartment(UpdateView):

    model = Appartment
    fields = '__all__'
    template_name_suffix ='_update_form'
    pk_url_kwarg = 'appartment_pk'
    success_url = reverse_lazy('edit-list-appartment')


# usuwanie apartamentu
class DeleteAppartment(DeleteView):

    model = Appartment
    pk_url_kwarg = 'appartment_pk'
    success_url = reverse_lazy('edit-list-appartment')


# dodawanie właściciela
class AddOwner(CreateView):
    model = Owner
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')


# dodawanie zdjęć do apartamentu
class AddAppartmentsPhoto(View):

    def get(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        form = AddAppartmentPhotoForm(instance=appartment)

        return render(request, "apprtrent/add_photos_form.html", {"form": form, "appartment": appartment, "button": "Dodaj zdjęcie"})

    def post(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        form = AddAppartmentPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.appartment = appartment
            photo.save()
            # return redirect(reverse('home'))
            return redirect(reverse('add-photo', kwargs={'appartment_id': photo.appartment_id}))
        return render(request, "apprtrent/add_photos_form.html", {"form": form, "button": "Dodaj zdjęcie"})


# pokazuje apartamenty klientom - z zaznaczonym best_app - home
class AppartmensView(View):
    def get(self, request):
        appartments = Appartment.objects.filter(best_app=True)
        photos = Photo.objects.all()                                # todo jak pobrać tylko zdjęcia wybranych apartamentóœ
        facilities = Facility.objects.all()
        return render(request, "apprtrent/display.html", {"appartments": appartments, "photos": photos, "facilities": facilities})


# pokazuje apartamenty tylko z wybranego miasta
class AppartmentsByCityView(View):
    def get(self, request, city):
        appartments = Appartment.objects.filter(address_city__appartment=city)
        return render(request, "apprtrent/display.html", {"appartments": appartments})


# # wybór miasta
# class ChooseCityView(View):
#     def get(self, request):
#         city = City.objects.all()
#         return render



# pokazuje wybrany apartament
class AppartmentView(View):
    def get(self, request, appartment_id):
        appartment = get_object_or_404(Appartment, pk=appartment_id)
        facilities = appartment.facilities.all()
        fees = appartment.fees.all()
        photos = appartment.photo_set.all()
        return render(request, "apprtrent/display_one.html", {"appartment": appartment, "facilities": facilities, "fees": fees, "photos": photos})








