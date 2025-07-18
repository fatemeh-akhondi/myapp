from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Question, TestCase, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "UserProfiles"
    
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

admin.site.register(Question)
admin.site.register(TestCase)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)