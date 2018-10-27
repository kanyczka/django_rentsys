from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from apprtrent.views import HomeView, SignUPView, AddAppartment, AddAppartmentsPhoto, AppartmentsView, \
    AppartmentView, ChangeAppartment, AddOwner, AppartmentsEditList, DeleteAppartment, \
    UpdateArticleView, ArticleEditList, ArticleView

app_name = 'apprtrent'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name="logout"),
    path('signup/', SignUPView.as_view(), name="signup"),

    path('add_appartment/', AddAppartment.as_view(), name="add-appartment"),
    path('update_appartment/<int:appartment_pk>', ChangeAppartment.as_view(), name="update-appartment"),
    path('delete_appartment/<int:appartment_pk>', DeleteAppartment.as_view(), name="delete-appartment"),
    path('appartment_edit_list/', AppartmentsEditList.as_view(), name="edit-list-appartment"),

    path('add_photo/<int:appartment_id>', AddAppartmentsPhoto.as_view(), name="add-photo"),
    path('add_owner/', AddOwner.as_view(), name="add-owner"),
    path('appartments/', AppartmentsView.as_view(), name="appartments"),
    path('appartments/<str:city>/', AppartmentsView.as_view(), name="appartments-by-city"),
    path('appartment/<int:appartment_id>', AppartmentView.as_view(), name="appartment"),
    path('appartment/<int:appartment_id>/<str:message>', AppartmentView.as_view(), name="appartment-message"),

    path('article/<int:pk>', ArticleView.as_view(), name='article' ),
    path('update_article/<int:article_pk>', UpdateArticleView.as_view(), name='update-article'),
    path('article_list/', ArticleEditList.as_view(), name='article-list'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
