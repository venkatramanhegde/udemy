from rest_framework import serializers
from .models import User, Courses, Webinar, Subjects, Tags, TagsAssociation, Video, SubjectAssociation, VideoAssociation


class LoginSerializer(serializers.Serializer):
    """This is the serializer used for logging in user"""
    email = serializers.EmailField(max_length=256, required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},  write_only=True, required=True
    )

    class Meta:
        model = User


class SignUpSerializer(serializers.Serializer):
    """This is the serializer used for signup in user"""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50, allow_null=True)
    password = serializers.CharField(max_length=256)
    is_instructor = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=True)
    first_name = serializers.CharField(max_length=40, allow_null=True)
    last_name = serializers.CharField(max_length=40, allow_null=True)
    contact_no = serializers.CharField(max_length=25, allow_null=True)

    class Meta:
        model = User
    def create(self, validated_data):
        add_user = User.objects.create(**validated_data)
        add_user.save()
        return add_user


class AddGetUpdateCourseSerializer(serializers.Serializer):
    """This is the serializer used for add update and get course"""

    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000, allow_null=True)
    tags_list = serializers.ListField()
    subject_list = serializers.ListField()


    class Meta:
        model = Courses
        fields = ('name', 'description', 'id', 'tags_list', 'subject_list', 'fees', 'duration')

    def create(self, validated_data):
        add_course = Courses.objects.create(**validated_data)
        add_course.created_by_id = self.context.get("user_id")
        add_course.save()
        return add_course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.fees = validated_data.get('fees', instance.fees)
        instance.duration = validated_data.get('duration', instance.duration)


class AddWebinarSerializer(serializers.Serializer):
    """This is the serializer used for add update and get webinar"""

    webinar_title = serializers.CharField(max_length=250, allow_null=False)
    video_title = serializers.CharField(max_length=500)
    video_link = serializers.FileField(allow_null=True)
    description = serializers.CharField(allow_null=True)
    date_time = serializers.DateTimeField(allow_null=True)
    # course_id = models.ForeignKey(Courses, null=False, related_name="video_course_id", on_delete=False)
    # instructor_id = serializers.ForeignKey(User, null=False, related_name="video_instructor_id", on_delete=False)
    class Meta:
        model = Webinar
        fields = ('webinar_title', 'video_title', "video_link", "description", "date_time")

    def create(self, validated_data):
        add_webinar = Webinar.objects.create(**validated_data)
        add_webinar.video_link = self.context.get("video_link")
        add_webinar.created_by_id = self.context.get("user_id")
        add_webinar.save()
        return add_webinar

    def update(self, instance, validated_data):
        instance.webinar_title = validated_data.get('webinar_title', instance.webinar_title)
        instance.video_title = validated_data.get('video_title', instance.video_title)
        instance.video_link = validated_data.get('video_link', instance.video_link)
        instance.description = validated_data.get('description', instance.description)
        instance.date_time = validated_data.get('date_time', instance.date_time)


class AddGetUpdateSubjectsSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000, allow_null=True)
    total_time = serializers.IntegerField(allow_null=True)
    class Meta:
        model = Subjects
        fields = ('description', "total_time")
    def create(self, validated_data):
        add_subject = Subjects.objects.create(**validated_data)
        add_subject.created_by_id = self.context.get("user_id")
        add_subject.save()
        return add_subject

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.description = validated_data.get('description', instance.description)
        instance.total_time = validated_data.get('total_time', instance.total_time)


class AddGetUpdateTagsSerializer(serializers.Serializer):
    tag = serializers.CharField(max_length=50)

    class Meta:
        model = Tags
        fields = ('tag',)

    def create(self, validated_data):
        add_tags = Tags.objects.create(**validated_data)
        add_tags.created_by_id = self.context.get("user_id")
        add_tags.save()
        return add_tags

    def update(self, instance, validated_data):
        instance.tag = validated_data.get('tag', instance.tag)


class AssociateTagsSerializer(serializers.Serializer):
    tag_id = serializers.IntegerField(allow_null=False)
    course_id = serializers.IntegerField()
    webinar_id = serializers.IntegerField()
    video_id = serializers.IntegerField()
    class Meta:
        model = TagsAssociation
        fields = ('tag_id', "course_id", 'webinar_id', 'video_id')
    def create(self, validated_data):
        if validated_data.get('course_id') != 0:
            add_tags = TagsAssociation.objects.create(tags_id=validated_data.get('tag_id'),
                                                      created_by_id=self.context.get("user_id"),
                                                      course_id=validated_data.get('course_id'),
                                                      course_tag=True, #webinar_id=0, video_id=0
                                                      )
            append_tag = Courses.objects.get(id=validated_data.get('course_id'))
            tag_name = Tags.objects.get(id=validated_data.get('tag_id'))
            try:
                append_tag.tags_list.append(tag_name.tag)
            except:
                append_tag.tags_list = [tag_name.tag]
            append_tag.save()
            # list(append_tag.tags_list).add(tag_name.tag)
        elif validated_data.get('webinar_id'):
            add_tags = TagsAssociation.objects.create(tags_id=validated_data.get('tag_id'),
                                                      created_by_id=self.context.get("user_id"),
                                                      webinar_id=validated_data.get('webinar_id'),
                                                      webinar_tag=True,
                                                      # video_id=0, course_id=0
                                                      )
            append_tag = Webinar.objects.get(id=validated_data.get('webinar_id'))
            tag_name = Tags.objects.get(id=validated_data.get('tag_id'))
            try:
                append_tag.tags_list.append(tag_name.tag)
            except:
                append_tag.tags_list = [tag_name.tag]
            append_tag.save()
        else:
            add_tags = TagsAssociation.objects.create(tags_id=validated_data.get('tag_id'),
                                                      created_by_id=self.context.get("user_id"),
                                                      video_id=validated_data.get('video_id'),
                                                      # webinar_id=0, course_id=0
                                                      )

        return add_tags

class AssociateSubjectsSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField(allow_null=False)
    course_id = serializers.IntegerField()
    webinar_id = serializers.IntegerField()
    video_id = serializers.IntegerField()
    class Meta:
        model = SubjectAssociation
        # fields = ('description', "total_time")
    def create(self, validated_data):
        if validated_data.get('course_id') !=0:
            add_sub = SubjectAssociation.objects.create(subject_id=validated_data.get('subject_id'),
                                                         created_by_id=self.context.get("user_id"),
                                                         course_id=validated_data.get('course_id'),
                                                         course_sub=True)

            append_sub = Courses.objects.get(id=validated_data.get('course_id'))
            sub_name = Subjects.objects.get(id=validated_data.get('subject_id'))
            try:
                append_sub.subject_list.append(sub_name.subject)
            except:
                append_sub.subject_list = [sub_name.subject]
            append_sub.save()

        elif validated_data.get('webinar_id') !=0:
            add_sub = SubjectAssociation.objects.create(subject_id=validated_data.get('subject_id'),
                                                      created_by_id=self.context.get("user_id"),
                                                      webinar_sub=True, video_id=validated_data.get('video_id'))
            append_sub = Webinar.objects.get(id=validated_data.get('webinar_id'))
            sub_name = Subjects.objects.get(id=validated_data.get('subject_id'))
            try:
                append_sub.subject_list.append(sub_name.subject)
            except:
                append_sub.subject_list = [sub_name.subject]
            append_sub.save()

        else:
            add_sub = SubjectAssociation.objects.create(subject_id=validated_data.get('subject_id'),
                                                      created_by=self.context.get("user_id"),
                                                      video_id=validated_data.get('video_id'))

        return add_sub


class VideoUploadSerializer(serializers.Serializer):
    video_tittle = serializers.CharField(max_length=250, allow_null=False)
    # video_path = serializers.CharField(max_length=250, allow_null=False)
    link = serializers.FileField()
    is_webinar = serializers.BooleanField(default=False)
    is_course = serializers.BooleanField(default=False)


    class Meta:
        model = Video
        fields = ('video_tittle', 'video_path', 'instructor_id', 'course_id', 'webinar_id', 'is_webinar',
                  'is_course',)
    def create(self, validated_data):
        # if validated_data.get('course_id'):
        add_subject = Video.objects.create(**validated_data,
                                       video_path=self.context.get('video_path'),
                                       created_by_id=self.context.get('user_id'),
                                       instructor_id = self.context.get('user_id'),
                                                 )
        return add_subject

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.description = validated_data.get('description', instance.description)
        instance.total_time = validated_data.get('total_time', instance.total_time)


class AssociateVideoSerializer(serializers.Serializer):
    video_id = serializers.IntegerField(allow_null=False)
    webinar_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    class Meta:
        model = VideoAssociation
        # fields = ('description', "total_time")
    def create(self, validated_data):
        if validated_data.get('course_id') != 0:
            print("tes")
            add_video = VideoAssociation.objects.create(video_id=validated_data.get('video_id'),
                                                      course_id=validated_data.get('course_id'))

        else:
            add_video = SubjectAssociation.objects.create(video_id=validated_data.get('video_id'),
                                                      created_by_id =int(self.context.get("user_id")),
                                                      webinar_id=validated_data.get('webinar_id'))

        add_video.save()
        return add_video

