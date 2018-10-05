from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
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
            # appartments = Appartment.objects.filter(address_city=city)
            return redirect(reverse('appartments-by-city', kwargs={'city': city}))
            # return render(request, "apprtrent/display.html", {"appartments": appartments})
        return render(request, "apprtrent/display.html", {"appartments": appartments, "form": form,
                                                          "cities": cities, "photos": photos})







# pokazuje wybrany apartament
class AppartmentView(View):
    def get(self, request, appartment_id):
        appartment = get_object_or_404(Appartment, pk=appartment_id)
        facilities = appartment.facilities.all()
        fees = appartment.fees.all()
        photos = appartment.photo_set.all()
        today = date.today()
        booked_already = appartment.booking_set.filter(checkout_date__gt=date.today())
        a = booked_already.count()

        days_notavailable = []
        if booked_already:
            for i in range(0, booked_already.count() - 1):
                for b in booked_already:
                    date_in = b.checkin_date
                    date_out = b.checkout_date
                    days = [date_in + timedelta(days=x) for x in range((date_out - date_in).days + 1)]
                    days_notavailable.append(days)

            # days = [datetime.strftime(dn, "%d-%m-%Y") for dn in days_notavailable]
                    # days.sort()
                    # days_notavailable = [datetime.strftime(dn, "%d-%m-%Y") for dn in days]

        form = AddBookingForm(instance=appartment)
        return render(request, "apprtrent/display_one.html", {"appartment": appartment,
                                                              "facilities": facilities,
                                                              "fees": fees, "photos": photos,
                                                              "booked_already": booked_already,
                                                              "days_notavailable": days_notavailable,
                                                              "today": today,
                                                              "form": form})
    def post(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        facilities = appartment.facilities.all()
        fees = appartment.fees.all()
        photos = appartment.photo_set.all()

        today = datetime.today().date()
        # today = today.strftime('%Y-%m-%d')
        booked_after_today = appartment.booking_set.filter(checkout_date__gte=today)
        form = AddBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.appartment = appartment
            booked_already = appartment.booking_set.filter(checkout_date__gt=booking.checkin_date)
            checkin_date = booking.checkin_date
            checkout_date = booking.checkout_date
            if checkin_date < today:
                message = f'Najwcześniejsza możliwa data rezerwacji, to {today}'
                return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                                      "facilities": facilities,
                                                                      "fees": fees, "photos": photos,
                                                                      "booked_already": booked_already,
                                                                      "today": today,
                                                                      "form": form})


            # days_booked = [checkin_date + timedelta(days=x) for x in range((checkout_date - checkin_date).days + 1)]

            for b in booked_already:
                date_in = b.checkin_date
                date_out = b.checkout_date
                if checkin_date < date_in and checkout_date> date_in and checkout_date < date_out or \
                        checkin_date > date_in and checkout_date < date_out or \
                    checkin_date > date_in and checkin_date < date_out:
                    message = "Ten termin został już zarezerwowany"

                    return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                                          "facilities": facilities,
                                                                          "fees": fees, "photos": photos,
                                                                          "booked_already": booked_already,
                                                                          "today": today,
                                                                          "form": form})
            try:
                booking.save()
            except IntegrityError:
                message = "Ten termin jest już zarezerwowany"
                return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                                      "facilities": facilities,
                                                                      "fees": fees, "photos": photos,
                                                                      "booked_already": booked_already,
                                                                      "today": today,
                                                                      "form": form})
            message = "Dokonano wstępnej rezerwacji, dziękujemy"
            return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                                  "facilities": facilities,
                                                                  "fees": fees, "photos": photos,
                                                                  "booked_already": booked_already,
                                                                  "today": today,
                                                                  "form": form})

            # return redirect(reverse('home'))






# # pokazuje wybrany apartament
# class AppartmentView(View):
#     def get(self, request, appartment_id):
#         appartment = get_object_or_404(Appartment, pk=appartment_id)
#         facilities = appartment.facilities.all()
#         fees = appartment.fees.all()
#         photos = appartment.photo_set.all()
#         today = date.today()
#         booked_already = appartment.booking_set.filter(checkout_date__gt=date.today())
#         a = booked_already.count()
#
#         days_notavailable = []
#         if booked_already:
#             for i in range(0, booked_already.count() - 1):
#                 for b in booked_already:
#                     date_in = b.checkin_date
#                     date_out = b.checkout_date
#                     days = [date_in + timedelta(days=x) for x in range((date_out - date_in).days + 1)]
#                     days_notavailable.append(days)
#                     a = b
#
#             # days = [datetime.strftime(dn, "%d-%m-%Y") for dn in days_notavailable]
#                     # days.sort()
#                     # days_notavailable = [datetime.strftime(dn, "%d-%m-%Y") for dn in days]
#
#         form = AddBookingForm(instance=appartment)
#         return render(request, "apprtrent/display_one.html", {"appartment": appartment,
#                                                               "facilities": facilities,
#                                                               "fees": fees, "photos": photos,
#                                                               "booked_already": booked_already,
#                                                               "days_notavailable": days_notavailable,
#                                                               "today": today,
#                                                               "form": form})
#     def post(self, request, appartment_id):
#         appartment = Appartment.objects.get(pk=appartment_id)
#         facilities = appartment.facilities.all()
#         fees = appartment.fees.all()
#         photos = appartment.photo_set.all()
#         today = datetime.today()
#         today = today.strftime('%Y-%m-%d')
#         booked_after_today = appartment.booking_set.filter(checkout_date__gte=today)
#         form = AddBookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.appartment = appartment
#             # booked_already = appartment.booking_set.filter(checkout_date__gt=booking.checkin_date)
#             days_notavailable = []
#             if booked_after_today:
#                 for i in range(0, len(booked_after_today)-1):
#                     for b in booked_after_today:
#                         date_in = b.checkin_date
#                         date_out = b.checkout_date
#                         days = [date_in + timedelta(days=x) for x in range((date_out - date_in).days + 1)]
#                         days_notavailable.append(days)
#
#                         # days = [datetime.strptime(dn, "%Y-%m-%d") for dn in days_notavailable]
#                         # days.sort()
#                         # days_notavailable_sorted = [datetime.strftime(dn, "%Y-%m-%d") for dn in days]
#
#             if not booked_after_today:      # jeżeli nie ma rezerwacji na ten lokal po dzisiejszym dniu
#                 form.save()
#                 return redirect(reverse('home'))
#
#             checkin_date = booking.checkin_date
#             checkout_date = booking.checkout_date
#             days_booked = [checkin_date + timedelta(days=x) for x in range((checkout_date - checkin_date).days + 1)]
#
#             if list(set(booked_after_today).intersection(set(days_booked))):
#                 return render(request, "apprtrent/display_one.html", {"appartment": appartment,
#                                                                       "facilities": facilities,
#                                                                       "fees": fees, "photos": photos,
#                                                                       "booked_after_today": booked_after_today,
#                                                                       "form": form})
#             booking.save()
#
#             return redirect(reverse('home'))
#         return render(request, "apprtrent/display_one.html", {"form": form, "button": "Dodaj zdjęcie"})  # jak przekazać znowu dane





