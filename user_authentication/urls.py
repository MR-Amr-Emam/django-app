from django.urls import path, include
from .views import *


urlpatterns = [
    path("login/", LoginView.as_view(), name="authenticate-login"),
    path("signup/", SignupView.as_view(), name="authenticate-signup"),
    path("logout/", logoutView.as_view(), name="authenticate-logout"),
    path("personal_information", PersonalUserApi.as_view(), name="authentication-personaluser"),
    path("profile_<str:username>/", UserApi.as_view(), name="authentication-user"),
    path("informationprofile_<str:username>/", UserInformationApi.as_view(), name="authentication-userinformation"),
    path("profileimage_<str:username>/", ProfileImage.as_view(), name="authentication-profileimage"),
    path("croppedprofileimage_<str:username>/", CroppedProfileImage.as_view(), name="authentication-croppedprofileimage"),
]
