from rest_framework import serializers

from django.contrib.auth.models import User

import os

from .models import *


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = ["bio", "profile_image", "cropped_profile_image", "profile_image_url", "cropped_image_url", "profile_page_url"]


    def update(self, instance, validated_data):
        try:
            validated_data["profile_image"]
            os.remove(instance.profile_image.path)
        except:
            pass
        try:
            validated_data["cropped_profile_image"]
            print(instance.cropped_profile_image.path)
            os.remove(instance.cropped_profile_image.path)
        except:
            pass
        return super().update(instance, validated_data)




class UserSerializer(serializers.ModelSerializer):
    user_information = UserInformationSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "user_information"]


    
    
    
