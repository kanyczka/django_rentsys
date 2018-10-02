"""RentSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from apprtrent.views import HomeView, SignUPView, AddAppartment, AddAppartmentsPhoto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name="logout"),
    path('signup/', SignUPView.as_view(), name="signup"),
    # path('appartments', AppartmentsView.as_View(), name="appartments"),
    # path('appartments/city', AppartmentCityView.as_View(), name="city-appartments"),
    # path('appartment/city/<int:id>', AppartmentView.as_View(), name="appartment"),
    path('add_appartment', AddAppartment.as_view(), name="add-appartment"),
    path('add_photo/<int:appartment_id>', AddAppartmentsPhoto.as_view(), name="add-photo")
    # path('user/)





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
