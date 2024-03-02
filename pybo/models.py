from django.db import models
from common.models import User
import os

from ckeditor.fields import RichTextField

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = content = RichTextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    file_upload = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.subject

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Advertisement(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(
        "프로필 이미지", upload_to="common/profile", blank=True, null=True)

    def __str__(self):
        return self.title
 