
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("api/post", views.post, name="post"),
    path("api/post/edit", views.edit, name="edit"),
    path("api/follow", views.follow, name="follow")
]
