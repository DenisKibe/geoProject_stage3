from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

#here we add a custom manager by subclassing BaseUserManager
#which uses an email as the unique identifier rather than username

class UserManager(BaseUserManager):
    def create_user(self,email, password,**extra_fields):
        """
        Create and save a User with the given email and password and role
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.is_staff= True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save()

        return user

    
#here we abstract the user model to modify some fields
#since we are ok with other fields in User model we use AbstractUser
#modify username field to allow blank
#modify email field to be unique
#add outlet_id field.

class User(AbstractUser):
    username = models.CharField(_('username'),max_length=100, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class StudentsModels(models.Model):
    """
    create students model
    """

    ACTIVITIES=[(1,'Music'),(2,'Football'),(3,'Drama'),(4,'Rugbay')]

    student_id = models.AutoField(_('identification number'),primary_key=True)
    first_name = models.CharField(_('first name'),max_length=20,blank=False)
    last_name = models.CharField(_('last name'),max_length=20,blank=False)
    profile_photo = models.URLField(_('image url'),blank=False)
    school_activities = models.PositiveSmallIntegerField(_('school activities'),choices=ACTIVITIES,blank=False)
    created_by = models.ForeignKey(get_user_model(),on_delete=models.RESTRICT)
    created_on = models.DateTimeField(_('created on'),auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'),auto_now=True)

    class Meta:
        db_table = 'students'


    def __int__(self):
        return self.student_id

