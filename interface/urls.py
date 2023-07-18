from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="interface-home"),
    path('submit_project/', SubmitPageView.as_view(), name="interface-submit_project"),
    path('login/', LoginView.as_view(), name="interface-login"),
    path('signup/', SignupView.as_view(), name="interface-signup"),
    path('profile_<str:username>/', ProfileView.as_view(), name="interface-profile"),
    path('notcomplete_projects/', ReviewProjectsView.as_view(), name="interface-projects"),
    path('reviewproject_<int:id>/', ProjectView.as_view(), name="interface-projectreview"),
    path('complete_projects/', CompleteProjects.as_view(), name="interface-completeprojects"),
    path('complete_project_<int:id>/', CompleteProject.as_view(), name="interface-completeproject"),
    path('search_result/', SearchProject.as_view(), name="interface-searchresult"),
]

