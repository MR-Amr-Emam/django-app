from django.urls import path
from .views import *

urlpatterns = [
    path('project_file_<int:id>/', GetFile.as_view(), name="projects-pdfile"),
    path("projects/", NonReviewedProjectsView.as_view(), name="projects-projects"),
    path("project_<int:id>/", ProjectView.as_view(), name="projects-project"),
    path("create_project/", CreateProjectView.as_view(), name="projects-create"),
    path("complete_projects/", CompleteProjectsView.as_view(), name="projects-completeprojects"),
    path("complete_project_<int:id>", CompleteProjectView.as_view(), name="projects-completeproject"),
    path("download_project_<int:id>", DownloadFile.as_view(), name="projects-downloadproject"),
    path("search_projects/", SearchProjectsView.as_view(), name="projects-searchprojects"),
]

