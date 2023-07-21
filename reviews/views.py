from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import PermissionDenied

from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated

import datetime, os, json

from .models import Review
from projects.models import Project

from .build_review_pdf import buildDoc



class ReturnReview(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        project = Project.objects.get(id=self.kwargs[self.lookup_field])
        if project.state == True:
            raise PermissionDenied()
        try:
            review = Review.objects.get(project=project)
            review.delete()
            review = Review.objects.create(project=project)
        except:
            review = Review.objects.create(project=project)

        return review


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


    def perform_create(self, serializer):
        review_id = serializer.validated_data["review_id"]
        review = Review.objects.get(id = review_id)
        try:
            Comment.objects.filter(general_comment=True, review=review).delete()
        except:
            pass
        serializer.save(review = review)


class FinishReview(generics.UpdateAPIView):
    serializer_class = FinishReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "id"

    def perform_update(self, serializer):
        review = serializer.save(reviewer=self.request.user, review_date=datetime.datetime.now())
        if review.project.state == True:
            raise PermissionDenied()
        comments = Comment.objects.filter(review=review, general_comment=False)
        general_comment = Comment.objects.filter(review=review, general_comment=True)[0]
        title = "reviewpdf-{}.pdf".format(review.id)
        buildDoc(review ,comments, title, general_comment, settings.BASE_DIR)
        review.review_pdf = reverse("review-pdfreview", args=[review.id])
        review.save()
        return review


class CompleteFinishReview(View):
    def put(self, request):
        data = json.loads(request.body)
        review_id = data["review_id"]
        state = data["state"]
        review = Review.objects.get(id=review_id)
        if request.user == review.reviewer:
            if state == True:
                review.project.state = True
                review.project.save()
            elif state == False:
                try:
                    review.delete()
                except:
                    pass
            return JsonResponse({"state":state})
        else:
            raise PermissionDenied()




class GetReviewFile(View):
    def get(self, request, **kwargs):
        id = kwargs["id"]
        review = Review.objects.get(id=id)
        review_location = os.path.join(settings.BASE_DIR, review.review_location).replace("\\", "/")
        with open(review_location, "rb") as file:
            file_response = HttpResponse(file.read(), headers={
                "Content-Type": "application/pdf",
                })
            return file_response


class DownloadReviewFile(View):
    def get(self, request, **kwargs):
        id = kwargs["id"]
        try:
            review = Project.objects.get(id=id).review
        except:
            return Http404("<h1>page not found</h1>")
        review_location = os.path.join(settings.BASE_DIR, review.review_location).replace("\\", "/")
        with open(review_location, "rb") as file:
            file_response = HttpResponse(file.read(), headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": 'attachment; filename="review-{}"'.format(review.project.project_file.name),
                })
            return file_response