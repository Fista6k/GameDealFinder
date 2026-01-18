from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.gameList, name="gameList"),
    path("games/<uuid:gameid>/", views.gameInfo, name="gameInfo"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("waitlist/", views.waitlist_view, name="waitlist"),
    path("waitlist/add/<uuid:gameid>/", views.add_to_waitlist, name="add_to_waitlist"),
    path("waitlist/remove/<uuid:gameid>/", views.remove_from_waitlist, name="remove_from_waitlist")
]