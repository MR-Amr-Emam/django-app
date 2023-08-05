from django.shortcuts import render
from django.views import View
from django.http import HttpResponseNotAllowed, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
class HomePageView(View):
    def get(self, request):
        return render(request, "home_page_template.html")


class SubmitPageView(View):
    def get(self, request):
        if request.user.is_authenticated == True:
            return render(request, "submit_page_template.html")
        else:
            return HttpResponseNotAllowed("<h1>you  login</h1>")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

class SignupView(View):
    def get(self, request):
        return render(request, "signup.html")

class ProfileView(View):
    def get(self, request, **kwargs):
        username = kwargs["username"]
        try:
            User.objects.get(username=username)
        except:
            raise Http404
        return render(request, "profile.html")
    
class ReviewProjectsView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated == False:
            return HttpResponseNotAllowed("<h1>you must login</h1>")
        if request.user.is_staff == True:
            return render(request, "review-projects.html")
        else:
            return HttpResponseNotAllowed("<h1> not allowed </h1>")

class ProjectView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated == False:
            return HttpResponseNotAllowed("<h1>you must login</h1>")
        if request.user.is_staff == True:
            return render(request, "review-project.html")
        else:
            return HttpResponseNotAllowed("<h1> not allowed </h1>")


class CompleteProjects(View):
    def get(self, request):
        return render(request, "complete-projects.html")


class CompleteProject(View):
    def get(self, request, **kwargs):
        return render(request, "projectview.html")


class SearchProject(View):
    def get(self, request, **kwargs):
        return render(request, "search.html")
    