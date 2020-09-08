
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>",views.profile,name="profile"),
    path("following",views.following,name="following"),


    #API routes
    path("post/<int:post_id>",views.post,name="post"),
    path("posts/<str:batchtype>/<int:pagenum>",views.posts,name="posts"),
    path("post",views.newpost,name="newpost"),
    path("follow/<str:pageusername>",views.follow,name="follow")
]
