from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from udemy.permision import IsInstructor, IsStudents
from udemy.settings import BASE_DIR
from .serializers import LoginSerializer, \
                        AddGetUpdateCourseSerializer,\
                        AddWebinarSerializer,\
                        AddGetUpdateSubjectsSerializer,\
                        AddGetUpdateTagsSerializer, \
                        AssociateTagsSerializer, \
                        VideoUploadSerializer,\
                        AssociateSubjectsSerializer, \
                        AssociateVideoSerializer,\
                        SignUpSerializer


from .models import Webinar, Subjects, Tags, Courses, Video, VideoAssociation, TagsAssociation, SubjectAssociation
# from common.exceptions import InvalidData
import logging
# Create your views here.
class LoginAPIView(APIView):
    """
    This class based api view is for login.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        This method takes 'email' and 'password'
        url: http://localhost:8000/appmanagment/login/

        """

        serializer = LoginSerializer(data=request.data)
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
        if user.is_instructor:
            # instructor can log in see all his courses and videos and number of views.
            login(request, user)
            # logout(request)

            print("super")
        else:
            pass
            # student can log in see all the courses and videos and webinars .
        return Response("User logedin successfull")



class SignUp(APIView):
    serializer_class = SignUpSerializer
    def post(self, request):
        """
                         url:appmanagment/sign_up/
                         This will for sign up to application
                """

        user_add = self.serializer_class(data=request.data)
        if user_add.is_valid():
            user_add.save()
            return Response({"msg": "user added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": user_add.errors}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class AddCourse(APIView):
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.
    serializer_class = AddGetUpdateCourseSerializer

    """
        This class based api view is to add update and to get webinar

        """
    def get(self, request):

        """
                 url:/appmanagment/add_course/
                 :return: this will return course data for the logged in instructor.
        """
        try:
            serializer = AddGetUpdateCourseSerializer(Courses.objects.filter(created_by_id=request.user.id), many=True)
            return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "something went wrong"})

    def post(self, request):
        """
                         url:appmanagment/add_course/
                         Course details will updated if id is present in request body else it will create
                         new Course.
                """

        if 'id' in request.data:
            courses = Courses.objects.filter(id=request.data['id']).first()
            if not courses:
                return Response({"msg": courses.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                update_course_serializer = AddGetUpdateCourseSerializer(courses, data=request.data)
            if not update_course_serializer.is_valid():
                return Response({"msg": courses.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "webinar updated successfully", "data": update_course_serializer.data},
                    status.HTTP_200_OK)

        else:
            course_add = self.serializer_class(data=request.data, context={"user_id": request.user.id})
            if course_add.is_valid():
                course_add.save()
                return Response({"msg": "course added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": course_add.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        course_obj = Courses.objects.get(id=request.data['course_id'])
        course_obj.delete()
        return Response({"msg": "course deleted successfully"})

from django.core.files.storage import FileSystemStorage
import os


class UploadWebinar(APIView):
    """
         This class based api view is to add update and to get webinar

         """
    serializer_class = AddWebinarSerializer
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.

    def get(self, request):
        """
                 url:/appmanagment/get_webinar/
                 :return: this will return webinar data for the logged in user.
        """
        webinar = Webinar.objects.filter(created_by_id=request.user.id).values_list('webinar_title', 'video_title',
                                                        'video_link', 'description', 'date_time')[:100][0]
        webinar = Webinar.objects.filter(created_by_id=request.user.id).first()
        print(webinar)
        try:
            serializer = AddWebinarSerializer(Webinar.objects.filter(created_by_id=request.user.id), many=True)
            return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "somthing went wrong"})

    def post(self, request):
        """
                         url:appmanagment/addcourse/
                         :return: this will return success message.
                         Course details will updated if id is present in request body else it will create
                         new Course.
                """
        if 'id' in request.data:
            webinar = Webinar.objects.filter(id=request.data['id']).first()
            if not webinar:
                return Response({"msg": webinar.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                update_webinar_serializer = AddWebinarSerializer(webinar, data=request.data)
            if not update_webinar_serializer.is_valid():
                return Response({"msg": webinar.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "webinar updated successfully", "data": update_webinar_serializer.data},
                    status.HTTP_200_OK)

        else:
            webinar_video = request.FILES.getlist('video_link')
            for files in webinar_video:
                # try:
                    folder = "media/webinar" + '/' + str(request.user.id)
                    fs = FileSystemStorage(location=folder)
                    filename = fs.save(files.name, files)
                    mediapath = settings.MEDIA_ROOT + "/" + "webinar" + '/' + str(request.user.id) + "/{}"
                    filepath = os.path.join(BASE_DIR, mediapath).format(filename)
                    saving_file_path = "webinar" + '/' + str(request.user.id) + '/' + filename
                    data = {"msg": "Feedback file succesfully saved."}
                    print(data , saving_file_path)
                # except Exception as e:
                #     print(e)
                #     data = {"msg": "video file not saved. please Upload again.", "status": 500}
            webinar_add = self.serializer_class(data=request.data, context={"user_id":
                                                                             request.user.id, "video_link": saving_file_path})
            if webinar_add.is_valid():
                webinar_add.save()
                return Response({"msg": "webinar created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": webinar_add.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddGetUpdateSubjects(APIView):
    """
         This class based api view is to add update and to get subjects

         """
    serializer_class = AddGetUpdateSubjectsSerializer
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.

    def get(self, request):
        """
                 url:/appmanagment/add_subjects/
                 :return: this will return subjects data for the logged in user.
        """
        try:
            serializer = AddGetUpdateSubjectsSerializer(Subjects.objects.filter(created_by_id=request.user.id), many=True)
            print(serializer.data)
            return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "something went wrong"})

    def post(self, request):
        """
                         url:appmanagment/addcourse/
                         :return: this will return success message.
                         subject details will updated if id is present in request body else it will create
                         new subject.
                """
        try:
            if 'id' in request.data:
                subject = Subjects.objects.filter(id=request.data['id']).first()
                if not subject:
                    return Response({"msg": subject.errors}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    update_subject_serializer = AddGetUpdateSubjectsSerializer(subject, data=request.data)
                if not update_subject_serializer.is_valid():
                    return Response({"msg": subject.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        {"message": "subjects updated successfully", "data": update_subject_serializer.data},
                        status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"msg": "something went wrong please try again"})



        else:
            try:
                subject_add = self.serializer_class(data=request.data, context={"user_id":request.user.id})
                if subject_add.is_valid():
                    subject_add.save()
                    return Response({"msg": "subjects created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"msg": subject_add.errors}, status=status.HTTP_400_BAD_REQUEST)

            except Exception:
                return Response({"msg": "something went wrong please try again"})


class AddGetUpdateTags(APIView):
    """
         This class based api view is to add update and to get tags

         """
    serializer_class = AddGetUpdateTagsSerializer
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.

    def get(self, request):
        """
                 url:/appmanagment/add_tags/
                 :return: this will return Tags data for the logged in user.
        """
        try:
            serializer = AddGetUpdateTagsSerializer(Tags.objects.filter(created_by_id=request.user.id), many=True)
            return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "something went wrong"})

    def post(self, request):
        """
                         url:appmanagment/add_tags/
                         :return: this will return success message.
                         Course details will updated if id is present in request body else it will create
                         new Course.
                """
        try:
            if 'id' in request.data:
                tag = Tags.objects.filter(id=request.data['id']).first()
                if not tag:
                    return Response({"msg": tag.errors}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    update_tag_serializer = AddGetUpdateSubjectsSerializer(tag, data=request.data)
                if not update_tag_serializer.is_valid():
                    return Response({"msg": tag.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        {"message": "tag updated successfully", "data": update_tag_serializer.data},
                        status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"msg": "something went wrong please try again"})



        else:
            try:
                tag_add = self.serializer_class(data=request.data, context={"user_id": request.user.id})
                if tag_add.is_valid():
                    tag_add.save()
                    return Response({"msg": "tag created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"msg": tag_add.errors}, status=status.HTTP_400_BAD_REQUEST)

            except Exception:
                return Response({"msg": "something went wrong please try again"})


class AssociateTags(APIView):
    """
            This class based api view is add tag to course or webinar

            """
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.
    serializer_class = AssociateTagsSerializer
    def get(self, request):
        try:
            serializer = AddGetUpdateTagsSerializer(Tags.objects.filter(created_by_id=request.user.id), many=True)
            return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "something went wrong"})
    def post(self, request):
        tag_add = self.serializer_class(data=request.data, context={"user_id": request.user.id})
        try:
            if tag_add.is_valid():
                tag_add.save()
                return Response({"msg": "tag added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": tag_add.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"msg": "something went wrong please try again"})


class AssociateSubjects(APIView):
    """
            This class based api view is add subject to course or webinar

            """
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.
    serializer_class = AssociateSubjectsSerializer
    def post(self, request):
        sub_add = self.serializer_class(data=request.data, context={"user_id": request.user.id})
        try:
            if sub_add.is_valid():
                sub_add.save()
                return Response({"msg": "subject added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": sub_add.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"msg": "something went wrong please try again"})


class VideoUpload(APIView):
    """
            This class based api view is when student log is

            """
    permission_classes = [IsInstructor] # Only Authenticated Instructor  can access this api.
    serializer_class = VideoUploadSerializer
    # def get(self, request):
    #     pass

    def post(self, request):
        try:
            video = request.FILES.getlist('link')
            print(request.data)
            for files in video:
                if 'is_webinar' in request.data:
                    folder = "media/webinar"
                    mediapath = settings.MEDIA_ROOT + "/" + "webinar" + "/{}"
                    # saving_file_path = "webinar" + '/' + filename
                elif 'is_course' in request.data:

                    folder = "media/course"
                    mediapath = settings.MEDIA_ROOT + "/" + "course" + "/{}"
                else:
                    folder = "media/videos" + '/' + str(request.user.id)
                    fs = FileSystemStorage(location=folder)
                    filename = fs.save(files.name, files)
                    mediapath = settings.MEDIA_ROOT + "/" + "videos" + '/' + str(request.user.id) + "/{}"
                    filepath = os.path.join(BASE_DIR, mediapath).format(filename)
                    saving_file_path = "videos" + '/' + str(request.user.id) + '/' + filename





            save_video = self.serializer_class(data=request.data,
                                               context={'video_path': saving_file_path, "user_id": request.user.id})
                                                        # "saving_video_path": saving_video_path})
            if save_video.is_valid():
                save_video.save()
                return Response({"msg": "video added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": save_video.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            data = {"msg": "video file not saved. please Upload again.", "status": 500}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssociateVideo(APIView):
    """
            This class based api view is add subject to course or webinar

            """
    permission_classes = [IsInstructor]  # Only Authenticated Instructor  can access this api.
    serializer_class = AssociateVideoSerializer
    def post(self, request):
        video_add = self.serializer_class(data=request.data, context={"user_id": request.user.id})
        try:
            if video_add.is_valid():
                video_add.save()
                return Response({"msg": "video added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": video_add.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"msg": "something went wrong please try again"})



class NumberOfViews(APIView):
    """
              This class based api see the most viewed videos, courses and webinars.

              """
    permission_classes = [IsInstructor]  # Only Authenticated Instructor  can access this api.
    def get(self, request):
        course = Courses.objects.filter(created_by_id=request.user.id).values_list("name", "description", 'tags_list', 'subject_list', "total_number_of_views").order_by("total_number_of_views")[:15]
        webinar = Webinar.objects.filter(created_by_id=request.user.id).values_list('id', "webinar_title", "video_title", 'tags_list', 'subject_list', 'video_link', "numbers_of_views").order_by("numbers_of_views")[:15]
        videos = Video.objects.filter(created_by_id=request.user.id).values_list('id',"video_tittle", "link", "numbers_of_views").order_by("numbers_of_views")[:15]

        video_views = Video.objects.all().values_list("video_tittle", "numbers_of_views")
        data = {"courses": course, "webinar": webinar, "videos": videos}
        return Response(data)


# I am showing most popular 15 courses  courses
class StudentPage(APIView):
    permission_classes = [IsStudents]  # Only Authenticated student  can access this api.
    def get(self, request):
        course = Courses.objects.filter(id__in = [i for i in range(100)]).values_list("name", "description", 'tags_list', 'subject_list').order_by("total_number_of_views")[:15]
        # webinar = Webinar.objects.filter().values_list("webinar_title", "video_title", 'tags_list', 'subject_list', 'video_link').order_by("total_number_of_views")[:15]
        videos = Video.objects.filter(Q(is_webinar=False) & Q(is_course=False)).values_list("video_tittle", "link").order_by("numbers_of_views")[:15]
        data = {"courses": course, "webinar": "webinar", "videos": videos}
        return Response(data)


# Note Here we can implement caching. To increase performance.
class StudentFilter(APIView):
    # permission_classes = [IsStudents]  # Only Authenticated Instructor  can access this api.
    def get(self, request):
        title = request.GET.get('skill')
        tag_id = Tags.objects.filter(tag=title).values_list("id")
        tag_course_id = TagsAssociation.objects.filter(tags_id__in=list(tag_id)).values_list("course_id")
        sub_id = Subjects.objects.filter(subject__icontains=title).values_list("id")
        sub_course_id = SubjectAssociation.objects.filter(subject_id__in=list(sub_id)).values_list("course_id")
        course = Courses.objects.filter(Q(name__icontains=title) |
                                        Q(id__in=[i[0] for i in list(sub_course_id)]) |
                                        Q(id__in=[i[0] for i in list(tag_course_id)])).values_list('id',
                                        "name", "description", 'tags_list', 'subject_list', 'total_number_of_views').order_by(
                                        "total_number_of_views")[:15]

        for i in list(course):
            count = Courses.objects.filter(id=i[0]).first().total_number_of_views +1
            Courses.objects.filter(id=i[0]).update(total_number_of_views=count)

        webinar = Webinar.objects.filter(Q(webinar_title__icontains=title) |
                                         Q(id__in=[i[0] for i in list(sub_course_id)]) |
                                         Q(id__in=[i[0] for i in list(tag_course_id)])).values_list('id',
                                         "webinar_title", "video_title", 'tags_list', 'subject_list', 'video_link', "numbers_of_views").order_by("numbers_of_views")[:15]

        for i in list(webinar):
            count = Webinar.objects.filter(id=i[0]).first().numbers_of_views +1
            Webinar.objects.filter(id=i[0]).update(numbers_of_views=count)
        videos = Video.objects.filter(video_tittle__icontains = title).values_list('id',"video_tittle", "link", "numbers_of_views").order_by("numbers_of_views")[:15]
        for i in list(videos):
            count = Video.objects.filter(id=i[0]).first().numbers_of_views +1
            Video.objects.filter(id=i[0]).update(numbers_of_views=count)

        data = {"courses": course, "webinar": webinar, "videos": videos}
        return Response(data)


class StudentSuggestions(APIView):
    def post(self, request):
        searched_skill = request.data.get('searched_skill')
        videos = Video.objects.filter(video_title__icontains=searched_skill).Values_list("video_tittle", "link").order_by("number_of_views")[:15]
        webinar = Webinar.objects.filter(webinar_title__icontains=searched_skill).Values_list("webinar_title", "video_title", "numbers_of_views",
                                                                "video_link").order_by("number_of_views")[:15]


class GetCourseVideo(APIView):
    def get(self, request):
        video_ids = VideoAssociation.objects.filter(course_id=request.GET["course_id"]).values_list("video_id", flat=True)

        videos_link = Video.objects.filter(id__in=list(video_ids)).values_list('video_path', flat=True)
        return Response({"data": videos_link})










