from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager

from django.utils.translation import ugettext_lazy as _
import os
# Create your models here.

def get_video_path(instance, associated_profile_path):
    return os.path.join('media/', associated_profile_path)


class User(AbstractBaseUser):
    """this tables consist information about user"""
    created_on = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True,
        verbose_name='email address',
        max_length=100,
        null=True
    )
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=256)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    is_active = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=25, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Courses(models.Model):
    name = models.CharField(max_length=50,)
    description = models.CharField(max_length=1000, null=True)
    # fees = models.IntegerField(null=True)
    # duration = models.CharField(max_length=15, null=True)
    total_number_of_views = models.IntegerField(default=0)
    tags_list = ArrayField(models.CharField(max_length=50), null=True)
    subject_list = ArrayField(models.CharField(max_length=50), null=True)
    videos_list = ArrayField(models.CharField(max_length=50), null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                     related_name='course_created_by',
                                     on_delete=False)
    modified_by = models.ForeignKey(User, null=True,
                                             related_name='course_modified_by',
                                             on_delete=False)
    is_webinar = models.BooleanField(default=False)


class Webinar(models.Model):
    webinar_title = models.CharField(max_length=100)
    video_title = models.CharField(max_length=100, null=True)
    numbers_of_views = models.IntegerField(default=0)
    video_link = models.FileField(upload_to=get_video_path, null=False)
    tags_list = ArrayField(models.CharField(max_length=50), null=True)
    subject_list = ArrayField(models.CharField(max_length=50), null=True)
    videos_list = ArrayField(models.CharField(max_length=50), null=True)
    description = models.CharField(max_length=500, null=True)
    date_time = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='webinar_created_by',
                                   on_delete=False)
    modified_by = models.ForeignKey(User, null=True,
                                    related_name='webinar_modified_by',
                                    on_delete=False)


class Video(models.Model):
    video_tittle = models.CharField(max_length=250, null=False)
    link = models.FileField(upload_to=get_video_path, max_length=500)
    video_path = models.CharField(max_length=500, null=True)
    # course_id = models.ForeignKey(Courses, null=False, related_name="video_course_id", on_delete=False)
    instructor = models.ForeignKey(User, null=False, related_name="video_instructor_id", on_delete=False)
    course = models.ForeignKey(Courses, null=True, on_delete=False)
    webinar = models.ForeignKey(Webinar, null=True,  on_delete=False)
    numbers_of_views = models.IntegerField(default=0)
    is_webinar = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='video_created_by',
                                   on_delete=False)
    modified_by = models.ForeignKey(User, null=True,
                                    related_name='video_modified_by',
                                    on_delete=False)


class Subjects(models.Model):
    subject = models.CharField(max_length=50, null=False, default="python" )
    description = models.CharField(max_length=1000, null=True)
    total_time = models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='tags_created_by',
                                   on_delete=False)
    modified_by = models.ForeignKey(User, null=True,
                                    related_name='tags_modified_by',
                                    on_delete=False)


class Tags(models.Model):
    tag = models.CharField(max_length=50, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='tags_created_by_user',
                                   on_delete=False)
    modified_by = models.ForeignKey(User, null=True,
                                    related_name='tags_modified_by_user',
                                    on_delete=False)


class TagsAssociation(models.Model):
    tags = models.ForeignKey(Tags, null=True, on_delete=False)
    course = models.ForeignKey(Courses, null=True, on_delete=False, related_name='tag_ass_course',)
    webinar = models.ForeignKey(Webinar, null=True, related_name='web_ass_course', on_delete=False)
    course_tag = models.BooleanField(default=False,)
    webinar_tag = models.BooleanField(default=False,)
    video = models.ForeignKey(Video, null=True, on_delete=False)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='tags_added_by',
                                   on_delete=False)
    created_on = models.DateTimeField(auto_now_add=True)


class SubjectAssociation(models.Model):
    subject = models.ForeignKey(Subjects, null=True, on_delete=False)
    course = models.ForeignKey(Courses, null=True, on_delete=False, related_name='sub_ass_course',)
    webinar = models.ForeignKey(Webinar, null=True, related_name='sub_ass_course',on_delete=False)
    course_sub = models.BooleanField(default=False,)
    webinar_sub = models.BooleanField(default=False,)
    video = models.ForeignKey(Video, null=True, on_delete=False)
    created_by = models.ForeignKey(User, null=True,
                                   related_name='sub_added_by',
                                   on_delete=False)
    created_on = models.DateTimeField(auto_now_add=True)


class VideoAssociation(models.Model):
    course = models.ForeignKey(Courses, null=True, on_delete=False)
    video = models.ForeignKey(Video, null=True, on_delete=False)
    webinar = models.ForeignKey(Webinar, null=True, on_delete=False)
    # created_by = models.ForeignKey(User, null=True,
    #                                related_name='video_added_by',
    #                                on_delete=False)
    # created_on = models.DateTimeField(auto_now_add=True)





