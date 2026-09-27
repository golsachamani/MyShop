from django.urls import path

from .views import (
    Register,
    UserLogin,
    UserLogout,
    Profile,
    PasswordChange,
    PasswordChangeDone,
)


urlpatterns = [

    path(
        "register/",
        Register.as_view(),
        name="register"
    ),

    path(
        "login/",
        UserLogin.as_view(),
        name="login"
    ),

    path(
        "logout/",
        UserLogout.as_view(),
        name="logout"
    ),

    path(
        "profile/",
        Profile.as_view(),
        name="profile"
    ),

    path(
        "password/",
        PasswordChange.as_view(),
        name="password_change"
    ),

    path(
        "password/done/",
        PasswordChangeDone.as_view(),
        name="password_change_done"
    ),
]