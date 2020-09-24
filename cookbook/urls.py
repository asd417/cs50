from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Authentication
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('',views.indexbase,name='indexbase'),
    path('index/<int:pagenum>', views.index,name='index'),
    path("profile/<str:username>/<int:pagenum>",views.profile,name='profile'),
    path("liked/",views.liked,name='liked'),
    path('search/',views.search,name='search'),

    #Recipe Views
    path('recipe/<int:id>',views.recipePage,name='recipe'),
    path('recipe/<int:id>/edit',views.recipeEditPage,name='recipeEdit'),
    path('upload/', views.createRecipe, name='upload'),

    #API
    path('getrecipe/<int:recipe_id>', views.getrecipe, name='getrecipe')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
