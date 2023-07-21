from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile, FileField
from django.conf import settings

import os


fs = FileSystemStorage(location = os.path.join(settings.BASE_DIR, "files/reviews"))


class ProjectFieldFile(FieldFile):
    @property
    def url(self):
        return "/reviews/comment_file_{}/".format(Comment.objects.get(image_comment=self).id)

class ProjectFileField(FileField):
    attr_class = ProjectFieldFile


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    review_date = models.DateTimeField(blank=True, null=True)
    accepted = models.BooleanField(default=False)
    review_pdf = models.URLField()

    @property
    def review_location(self):
        return "files/reviews/reviewpdf-{}.pdf".format(self.id)

    @property
    def reviewer_name(self):
        return self.reviewer.username



class Comment(models.Model):
    image_comment = models.ImageField(storage=fs, blank=True)
    rate = models.TextField(blank=False, null=False, choices=[
        ("amazing","Amazing"),
        ("very-well","Very well"),
        ("good","Good"),
        ("weak","Weak"),
        ])
    comment = models.TextField(blank=False, null=False)
    general_comment = models.BooleanField(default=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)