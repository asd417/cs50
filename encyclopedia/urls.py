from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entryname>", views.entry, name="entry"),
    path("<str:entryname>/edit",views.entryEdit, name="editPage"),
    path("search/results",views.search,name="search"),
    path("create/newpage",views.createPage,name="createPage"),
    path("random/redirect",views.randomPage,name="randomPage")
]
