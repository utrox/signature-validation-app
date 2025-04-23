from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from .models import User, UserProfile

# Register your models here.
#admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(UserProfile, ModelAdmin)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    user_profile = UserProfile


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
