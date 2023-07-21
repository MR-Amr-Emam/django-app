from rest_framework import generics, permissions
from .serializers import *

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from .models import *
import os

class CanChangeUser(permissions.BasePermission):
    def has_object_permission(self, request, view, instance):
        if request.method not in permissions.SAFE_METHODS:
            if request.user != instance:
                return False
        return True


class CanChangeUserInformation(permissions.BasePermission):
    def has_object_permission(self, request, view, instance):
        print(instance)
        if request.method not in permissions.SAFE_METHODS:
            if request.user != instance.user:
                return False
        return True


class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect("interface-home")



class LoginView(View):
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = user.user_information.profile_page_url
            return JsonResponse({"url":url})
        else:
            return JsonResponse({"error": "password does not match username"})


class SignupView(View):
    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        errors = {}

        if password != confirm_password:
            errors["confirm-password"] = "passwords do not match"
        if len(username) < 5:
            errors["username"] = "less than 5 characters"
        if len(password) < 5:
            errors["password"] = "less than 5 charcaters"

        if errors:
            errors["result"] = "negative"
            return JsonResponse(errors)
        else:
            if User.objects.filter(username=username).exists():
                return JsonResponse({"username":"this username is already used", "result":"negative"})
            for user in User.objects.all():
                if user.check_password(password):
                    return JsonResponse({"password":"this password is to simillar", "result":"negative"})
            user = User.objects.create_user(username=username, email=email, password=password)
            UserInformation.objects.create(user=user)
            login(request, user)
            response = {"result":"positive", "username":user.username}
            return JsonResponse(response)


class PersonalUserApi(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        try:
            user = User.objects.get(username=self.request.user.username)
        except:
            user = None
        return user


class UserApi(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = [CanChangeUser]


class UserInformationApi(generics.RetrieveUpdateAPIView):
    queryset = UserInformation.objects.all()
    serializer_class = UserInformationSerializer
    lookup_field = "username"
    permission_classes = [CanChangeUserInformation]

    def get_object(self):
        username = self.kwargs["username"]
        return UserInformation.objects.get(user=User.objects.get(username=username))


class ProfileImage(View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs["username"])
        image = user.user_information.profile_image


        try:
            with image.open("rb") as image:
                response = HttpResponse(image.read(), headers={
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'inline; filename="profile.jpg"',
                })
                return response
        except:
            print("nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            with open(os.path.join(settings.BASE_DIR, "files/user_information/defaultprofileimage.jpg"),"rb") as image:
                response = HttpResponse(image.read(), headers={
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'inline; filename="profile.jpg"',
                })
                return response


class CroppedProfileImage(View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs["username"])
        image = user.user_information.cropped_profile_image


        try:
            with image.open("rb") as image:
                response = HttpResponse(image.read(), headers={
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'inline; filename="profile.jpg"',
                })
                return response
        except:
            print("nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            with open(os.path.join(settings.BASE_DIR, "files/user_information/defaultcroppedprofile.jpg"), "rb") as image:
                response = HttpResponse(image.read(), headers={
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'inline; filename="profile.jpg"',
                })
                return response

