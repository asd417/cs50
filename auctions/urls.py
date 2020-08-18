from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("category/<int:cat_name>",views.category,name="category"),
    path("createListing",views.createListing,name="createListing")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)