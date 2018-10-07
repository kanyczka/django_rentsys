from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from datetime import date, timedelta, datetime
from django.db import IntegrityError

from apprtrent.forms import AddAppartmentPhotoForm, UserCreationForm2, AddAppartmentForm, AddBookingForm, \
    SearchAppartmentsInCity, SearchAppartmentsInCityCodersLabDist
from apprtrent.models import Appartment, Photo, Facility, Owner, City, Booking


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
        appartments = Appartment.objects.all().order_by("address_city")
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


# pokazuje apartamenty na stronie głównej, wszystkie lub w danym mieście
# class AppartmensViewByCodersLabDist(View):
#     def get(self, request, city, distance=None):
#         if distance:
#             appartments = Appartment.objects.filter(address_city=city).filter(distance=distance)
#         else:
#             appartments = Appartment.objects.filter(address_city=city)
#         cities = City.objects.all()
#         photos = Photo.objects.all()
#         form = SearchAppartmentsInCityCodersLabDist()
#         return render(request, "apprtrent/display.html", {"appartments": appartments, "form": form,
#                                                           "cities": cities, "photos": photos,
#                                                           "city": city, "distance": distance})
#     def post(self, request, city, distance=None):
#         form = SearchAppartmentsInCityCodersLabDist(request.POST)
#         city = City.objects.get(city_name=city)
#         appartments = Appartment.objects.filter(address_city=city)
#         if form.is_valid():
#             distance = form.cleaned_data['distance']
#             return redirect(reverse('appartments-by-city-and-distance', kwargs={'city': city,
#                                                                                     'distance': distance}))
#         else:
#             photos = Photo.objects.all()
#             return render(request, "apprtrent/display.html", {"appartments": appartments, "form": form,
#                                                           "photos": photos, "city": city, "distance": distance})


# pokazuje apartamenty na stronie głównej, wszystkie lub w danym mieście
class AppartmensView(View):
    def get(self, request, city=None):
        if city:
            city = City.objects.get(city_name=city)
            appartments = Appartment.objects.filter(address_city=city)
        else:
            appartments = Appartment.objects.all()
        cities = City.objects.all()
        photos = Photo.objects.all()
        form = SearchAppartmentsInCity()
        return render(request, "apprtrent/display.html", {"appartments": appartments, "form": form,
                                                          "cities": cities, "photos": photos})
    def post(self, request, city=None):
        form = SearchAppartmentsInCity(request.POST)
        appartments = Appartment.objects.all()
        cities = City.objects.all()
        photos = Photo.objects.all()
        if form.is_valid():
            city = form.cleaned_data['address_city']
            return redirect(reverse('appartments-by-city', kwargs={'city': city}))
        return render(request, "apprtrent/display.html", {"appartments": appartments, "form": form,
                                                          "cities": cities, "photos": photos})


# pokazuje wybrany apartament z możliwością jego rezerwacji
class AppartmentView(View):
    def get(self, request, appartment_id, message=None):
        if message:
            message = message
        appartment = get_object_or_404(Appartment, pk=appartment_id)
        facilities = appartment.facilities.all()
        fees = appartment.fees.all()
        photos = appartment.photo_set.all()
        today = date.today()
        booked_already = appartment.booking_set.filter(checkout_date__gt=date.today())
        # form = AddBookingForm({'appartment': appartment})
        form = AddBookingForm(instance=appartment)
        return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                              "facilities": facilities,
                                                              "fees": fees, "photos": photos,
                                                              "booked_already": booked_already,
                                                              "today": today,
                                                              "form": form})
    def post(self, request, appartment_id, message=None):
        appartment = Appartment.objects.get(pk=appartment_id)
        facilities = appartment.facilities.all()
        fees = appartment.fees.all()
        photos = appartment.photo_set.all()
        today = datetime.today().date()
        # today = today.strftime('%Y-%m-%d')
        form = AddBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.appartment = appartment
            booked_already_after_checkin = appartment.booking_set.filter(checkout_date__gt=booking.checkin_date)
            checkin_date = booking.checkin_date
            checkout_date = booking.checkout_date
            if checkin_date < today:
                message = f'Rezerwacje wstecz nie są możliwe. Wybierz wolny termin po {today}'
                return redirect(reverse('appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))

            # days_booked = [checkin_date + timedelta(days=x) for x in range((checkout_date - checkin_date).days + 1)]
            #  sprawdza czy temrmin jest już zajęty, jeżeli są jakieś rezerwacje po dacie check_in
            if booked_already_after_checkin:
                for b in booked_already_after_checkin:
                    date_in = b.checkin_date
                    date_out = b.checkout_date
                    if checkin_date <= date_in and checkout_date > date_in and checkout_date < date_out or \
                        checkin_date >= date_in and checkout_date <= date_out or \
                        checkin_date >= date_in and checkin_date <= date_out or \
                        checkin_date <= date_in and checkout_date >= date_out:
                        message = "Ten termin został już zarezerwowany"
                        return redirect(reverse('appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))
            try:

                booking.save()
            except IntegrityError:
                message = "Ten termin jest już zarezerwowany - Integrity"
                return redirect(reverse('appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))

            message = "Dokonano wstępnej rezerwacji, dziękujemy"
            return redirect(reverse('appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))
        else:
            message = "Błędna data, spróbuj ponownie"
        return redirect(reverse('appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))









