from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import ImageField, ImageFieldFile
from django.urls import reverse
from django.conf import settings

import os

class CroppedImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        user = self.instance.user
        return "/authenticate/croppedprofileimage_{}".format(user.username)


class CroppedImageImageField(ImageField):
    attr_class = CroppedImageFieldFile

class ProfileImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        user = self.instance.user
        return "/authenticate/profileimage_{}".format(user.username)

class ProfileImageImageField(ImageField):
    attr_class = ProfileImageFieldFile


fs = FileSystemStorage(location = os.path.join(settings.BASE_DIR, "files/user_information"))


##models


class UserInformation(models.Model):
    user = models.OneToOneField(User, related_name="user_information", on_delete=models.CASCADE)
    profile_image = ProfileImageImageField(storage=fs, default=os.path.join(settings.BASE_DIR, "files/user_information/defaultprofileimage.jpg"))
    bio = models.TextField(blank=True, null=True, default="")
    cropped_profile_image = CroppedImageImageField(storage=fs, default=os.path.join(settings.BASE_DIR, "files/user_information/defaultcroppedprofile.jpg"))

    @property
    def profile_image_url(self):
        return self.profile_image.url

    @property
    def cropped_image_url(self):
        return self.cropped_profile_image.url

    @property
    def profile_page_url(self):
        return reverse("interface-profile", kwargs={"username":self.user.username})
