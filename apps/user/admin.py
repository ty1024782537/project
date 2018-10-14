from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'phone', 'head', 'birthday', 'school_name']
