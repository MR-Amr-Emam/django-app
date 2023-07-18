from django.urls import path
from .views import *


urlpatterns = [
    path("review_<int:id>/", ReturnReview.as_view(), name="reviews-review"),
    path("comment/", CreateComment.as_view(), name="reviews-comment"),
    path("finish_review_<int:id>/", FinishReview.as_view(), name="review-finish"),
    path("pdfreview_<int:id>/", GetReviewFile.as_view(), name="review-pdfreview"),
    path("complete_finishreview", CompleteFinishReview.as_view(), name="review-completefinishreview"),
    path("download_review_<int:id>", DownloadReviewFile.as_view(), name="review-downloadreview"),
]

