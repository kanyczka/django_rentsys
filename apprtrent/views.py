from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from datetime import date, datetime
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

from apprtrent.forms import AddAppartmentPhotoForm, UserCreationForm2, AddAppartmentForm, AddBookingForm, \
    SearchAppartmentsInCity
from apprtrent.models import Appartment, Photo, Facility, Owner, City, Booking, Article


# Home
class Home(View):

    def get(self, request):
        return render(request, 'apprtrent/home.html')


# Tworzenie nowego usera
class SignUPView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'apprtrent/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('apprtrent:home'))
        return render(request, 'apprtrent/signup.html', {'form': form})


class ArticleView(DetailView):
    model = Article
    template_name = 'apprtrent/display_article.html'


class ArticleEditList(ListView):
    template_name = 'apprtrent/article_edit_list.html'

    def get_queryset(self):
        return Article.objects.all()


class UpdateArticleView(UpdateView):
    model = Article
    fields = '__all__'
    template_name_suffix = '_update_form'
    pk_url_kwarg = "article_pk"
    success_url = reverse_lazy('apprtrent:article-list')


# lista apartamentów do edycji
class AppartmentsEditList(View):
    def get(self, request):
        appartments = Appartment.objects.all().order_by("address_city")
        photos = Photo.objects.all()
        return render(request, "apprtrent/appartment_edit_list.html", {"appartments": appartments, "photos": photos})


# dodawanie apartamentu (z ograniczonymi uprawnieniami)
class AddAppartment(PermissionRequiredMixin, View):
    permission_required = 'apprtrent.new_appartment'

    def get(self, request):
        form = AddAppartmentForm()
        return render(request, "apprtrent/appartment_create_form.html", {"form": form})

    def post(self, request):
        form = AddAppartmentForm(request.POST)
        if form.is_valid():
            appartment = form.save()
            return redirect(reverse('apprtrent:add-photo', args=[appartment.id]))
        return render(request, "apprtrent/appartment_create_form.html", {"form": form})


# edycja i zmiana danych w apartamentcie
class ChangeAppartment(PermissionRequiredMixin, UpdateView):
    permission_required = 'apprtrent.change_appartment'

    model = Appartment
    fields = '__all__'
    template_name_suffix = '_update_form'
    pk_url_kwarg = 'appartment_pk'
    success_url = reverse_lazy('apprtrent:edit-list-appartment')


# usuwanie apartamentu
class DeleteAppartment(PermissionRequiredMixin, DeleteView):
    permission_required = 'apprtrent.delete_appartment'

    model = Appartment
    pk_url_kwarg = 'appartment_pk'
    success_url = reverse_lazy('apprtrent:edit-list-appartment')


# dodawanie właściciela
class AddOwner(PermissionRequiredMixin, CreateView):
    permission_required = 'apprtrent.add_owner'

    model = Owner
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('apprtrent:home')


# dodawanie zdjęć do apartamentu
class AddAppartmentsPhoto(View):

    def get(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        photos = appartment.photo_set.all()
        form = AddAppartmentPhotoForm(instance=appartment)

        return render(request, "apprtrent/add_photos_form.html",
                      {"form": form, "appartment": appartment, "photos": photos, "button": "Dodaj zdjęcie"})

    def post(self, request, appartment_id):
        appartment = Appartment.objects.get(pk=appartment_id)
        form = AddAppartmentPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.appartment = appartment
            if request.user.has_perm('apprtrent.can_add_photo'):
                photo.save()
            else:
                raise PermissionDenied("Access denied")
            return redirect(reverse('apprtrent:add-photo', kwargs={'appartment_id': photo.appartment_id}))
        return render(request, "apprtrent/add_photos_form.html", {"form": form, "button": "Dodaj zdjęcie"})


# pokazuje apartamenty na stronie głównej, wszystkie lub w danym mieście
class AppartmentsView(View):
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
            return redirect(reverse('apprtrent:appartments-by-city', kwargs={'city': city}))
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
        booked_already = appartment.booking_set.filter(checkout_date__gt=date.today()).order_by("checkin_date")
        first_booked = today
        if booked_already:
            for b in booked_already:
                checkin_date = b.checkin_date
                checkout_date = b.checkout_date
                if checkout_date - (checkout_date - checkin_date) <= first_booked:
                    first_booked = checkout_date
        form = AddBookingForm(instance=appartment, initial={"checkin_date": first_booked})
        return render(request, "apprtrent/display_one.html", {"message": message, "appartment": appartment,
                                                              "facilities": facilities, "fees": fees, "photos": photos,
                                                              "booked_already": booked_already,
                                                              "today": today, "form": form})

    def post(self, request, appartment_id, message=None):
        appartment = Appartment.objects.get(pk=appartment_id)
        today = datetime.today().date()
        form = AddBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.appartment = appartment
            booked_already_after_checkin = appartment.booking_set.filter(checkout_date__gt=booking.checkin_date)
            checkin_date = booking.checkin_date
            checkout_date = booking.checkout_date
            if checkin_date < today:
                message = f'Rezerwacje wstecz nie są możliwe. Wybierz wolny termin po {today}'
                return redirect(reverse('apprtrent:appartment-message',
                                        kwargs={'appartment_id': appartment_id, 'message': message}))

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
                        return redirect(reverse('apprtrent:appartment-message',
                                                kwargs={'appartment_id': appartment_id, 'message': message}))
            try:
                booking.save()
            except IntegrityError:
                message = "Ten termin jest już zarezerwowany"
                return redirect(reverse('apprtrent:appartment-message',
                                        kwargs={'appartment_id': appartment_id, 'message': message}))

            message = "Dokonano wstępnej rezerwacji, dziękujemy"
            return redirect(
                reverse('apprtrent:appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))

        else:
            message = "Błędna data, spróbuj ponownie"

        return redirect(
            reverse('apprtrent:appartment-message', kwargs={'appartment_id': appartment_id, 'message': message}))

# todo poprawić linki z url na 'apprtrent: urlname'
