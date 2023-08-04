from django.db import models
from django.db.models.fields.files import FieldFile, FileField
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

import os


class ProjectFieldFile(FieldFile):
    @property
    def url(self):
        return "/projects/project_file_{}/".format(self.instance.id)

class ProjectFileField(FileField):
    attr_class = ProjectFieldFile

fs = FileSystemStorage(location = os.path.join(settings.BASE_DIR, "files/projects"))


class Project(models.Model):
    project_file = ProjectFileField(storage=fs, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    assignment_date = models.DateTimeField(auto_now_add=True)

    @property
    def review_project_page_url(self):
        return reverse("interface-projectreview", kwargs={"id":self.id})

    @property
    def publisher_username(self):
        return self.publisher.username

    @property
    def project_page_url(self):
        return reverse("interface-completeproject", kwargs={"id":self.id})

    @property
    def profile_url(self):
        return reverse("interface-profile", kwargs={"username": self.publisher.username})



