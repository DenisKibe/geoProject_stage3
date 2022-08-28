from rest_framework import serializers
from django.contrib.auth import get_user_model
from mainapp_apis.models import StudentsModels
from django.contrib.auth.hashers import make_password
from django.conf import settings
import uuid, os
from django.core.files.storage import FileSystemStorage

UserModel=get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    """
    serializer to validate students details
    """
    ACTIVITIES=[(1,'Music'),(2,'Football'),(3,'Drama'),(4,'Rugbay')]

    student_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=20,required=True)
    last_name = serializers.CharField(max_length=30,required=True)
    profile_photo = serializers.URLField(read_only=True)
    school_activities = serializers.ChoiceField(choices=ACTIVITIES,required=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = StudentsModels
        fields = ('student_id','first_name','last_name','profile_photo','school_activities','created_by','created_on','updated_on')


    def create(self,validated_data):
        #set created_by
        validated_data['created_by']= self.context['request'].user

        #try upload image
        try:
            file = self.context['request'].FILES['image']
            file_name = file.name

            # validate the file exists
            if file_name is None:
                raise Exception('No File was uploaded.')

            if file_name.rsplit('.', 1)[1].lower() in settings.ALLOWED_FILE_EXTENSIONS:
                newFilename = str(uuid.uuid4())+'.'+file_name.rsplit('.', 1)[1].lower()

                fss = FileSystemStorage()
                file = fss.save(newFilename, file)

                fileurl = os.path.join(settings.MEDIA_ROOT, file)
                
                #set the profile_photo field to a url
                validated_data['profile_photo']=fileurl

                
            else:
                raise Exception('File extension is not supported.')

        except Exception as e:
            #on error set the url to a default
            validated_data['profile_photo']=os.path.join(settings.MEDIA_ROOT, 'default_avatar.jpg')

        studentDetail= StudentsModels.objects.create(**validated_data)

        return studentDetail

    #we define the get_method to get created by details
    def get_created_by(self,instance):
        return {'user':instance.created_by.email}


class TeacherSerializer(serializers.ModelSerializer):
    """
    serializer to validate students details
    """

    class Meta:
        model = UserModel
        fields = ('email','password')

        def create(self,validated_data):
            auth_user = UserModel.objects.create_user(**validated_data)
            return auth_user