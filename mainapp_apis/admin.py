from django.contrib import admin
from mainapp_apis.models import StudentsModels, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(StudentsModels)
class Admin_Students(admin.ModelAdmin):
    list_display = ['first_name','last_name','profile_photo','school_activities','created_by','created_on','updated_on']