from rest_framework import serializers

from django.contrib.auth.models import User

from .models import *


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = ["bio", "profile_image", "cropped_profile_image", "profile_image_url", "cropped_image_url", "profile_page_url"]


class UserSerializer(serializers.ModelSerializer):
    user_information = UserInformationSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "user_information"]


    
    
    
