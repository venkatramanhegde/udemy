from django.conf.urls import url
from .views import LoginAPIView, AddCourse, UploadWebinar, AddGetUpdateSubjects,\
    AddGetUpdateTags, VideoUpload, AssociateTags, AssociateSubjects, NumberOfViews, GetCourseVideo,\
    AssociateVideo, StudentPage, StudentFilter, SignUp

urlpatterns=[
    url(r'^login/', view=LoginAPIView.as_view(), name="login"),
    url(r'^sign_up/', view=SignUp.as_view(), name="sign-up"),

    url(r'^add_course/', view=AddCourse.as_view(), name="add-course"),
    url(r'^add_webinar/', view=UploadWebinar.as_view(), name="add-webinar"),
    url(r'^add_subject/', view=AddGetUpdateSubjects.as_view(), name="add-subject"),
    url(r'^add_tags/', view=AddGetUpdateTags.as_view(), name="add-tags"),
    url(r'^add_video/', view=VideoUpload.as_view(), name="add-video"),
    url(r'^associate_tag/', view=AssociateTags.as_view(), name="associate-tag"),
    url(r'^associate_sub/', view=AssociateSubjects.as_view(), name="associatesub"),
    url(r'^associate_video/', view=AssociateVideo.as_view(), name="associatesub"),
    url(r'^get_course_video/', view=GetCourseVideo.as_view(),
        name='course-id'),
    url(r'^number_of_views/', view=NumberOfViews.as_view(), name="numberofviews"),
    url(r'^student_page/', view=StudentPage.as_view(), name="student-page"),
    url(r'^student_filter/', view=StudentFilter.as_view(), name="student-filter"),

]