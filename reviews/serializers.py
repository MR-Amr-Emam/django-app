from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ["id", "project"]


class CommentSerializer(serializers.ModelSerializer):
    review_id = serializers.IntegerField(required=True)
    class Meta:
        model = Comment
        exclude = ["review"]


class FinishReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["accepted", "review_pdf"]
        read_only_fields = ["review_pdf"]
    

class CompleteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review_date", "accepted", "review_pdf", "reviewer_name"]