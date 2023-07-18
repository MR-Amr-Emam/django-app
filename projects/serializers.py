from rest_framework import serializers
from projects.models import *
from reviews.serializers import CompleteReviewSerializer

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_file", "description"]

class ProjectRetrieveAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id" ,"assignment_date", "publisher_username", "description", "review_project_page_url"]

class ProjectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_file", "description", "publisher", "state", "assignment_date", "review_project_page_url","publisher_username"]


class CompleteProjectSerializer(serializers.ModelSerializer):
    review = CompleteReviewSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ["id" , "description", "project_file", "project_page_url", "publisher_username", "assignment_date", "profile_url", "review"]