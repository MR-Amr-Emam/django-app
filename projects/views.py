from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.db.models import Q

from .models import Project

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from projects.models import *
from .serializers import *


class GetFile(View):
    def get(self, request, **kwargs):
        try:
            id = kwargs["id"]
            project = Project.objects.get(id=id)
            file = project.project_file
        except:
            raise Http404("page not found")
        
        if project.state == True:
            with file.open("rb") as file:
                file_response = HttpResponse(file.read(), headers={
                    "Content-Type": "application/pdf",
                    })
                return file_response
            
        if request.user.is_authenticated == False:
            raise Http404("page not found")
        
        if request.user.is_staff == True:
            with file.open("rb") as file:
                file_response = HttpResponse(file.read(), headers={
                    "Content-Type": "application/pdf",
                    })
                return file_response

        raise Http404("page not found")


class DownloadFile(View):
    def get(self, request, **kwargs):
        try:
            project = Project.objects.get(id=kwargs["id"])
        except:
            return Http404("<hi> page not found </h1>")
        if project.state == True:
            project_file = project.project_file
            with project_file.open("rb") as file:
                return HttpResponse(file.read(), headers={
                    "Content-Type":"application/pdf",
                    "Content-Disposition": 'attachment; filename="{}"'.format(project.project_file.name),
                })
        else:
            return Http404("<hi> page not found </h1>")
        




class NonReviewedProjectsView(generics.ListAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectRetrieveAllSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(state=False)


class ProjectView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Project.objects.all()
    lookup_field = "id"
    serializer_class = ProjectRetrieveSerializer


class CreateProjectView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data["project_file"].name.split(".")[-1] == "pdf":
            project = serializer.save(publisher=self.request.user)
            return project
        else:
            raise PermissionDenied


class CompleteProjectsView(generics.ListAPIView):
    queryset = Project.objects.filter(state=True)
    serializer_class = CompleteProjectSerializer


class CompleteProjectView(generics.RetrieveAPIView):
    queryset = Project.objects.filter(state=True)
    serializer_class = CompleteProjectSerializer
    lookup_field = "id"


class SearchProjectsView(generics.GenericAPIView):
    def get(self, request):
        try:
            lookup = request.GET["lookup"]
            projects = Project.objects.filter(Q(publisher__username__icontains=lookup)
            |Q(description__icontains=lookup), state=True)
            data = []
            for project in projects:
                data.append(CompleteProjectSerializer(project).data)
            return Response(data)
        except:
            return Response({})
    
