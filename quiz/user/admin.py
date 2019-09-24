from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.module_loading import import_module

import_module('test', package='quiz')
from tests.models import Score


class ScoreInline(admin.TabularInline):
    model = Score
    readonly_fields = ["test", "count_right", "count_wrong", "percentage_correct_answers"]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'information', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ['email', 'username', 'birth_date', 'information', 'profile_image']
    inlines = [
        ScoreInline,
    ]


admin.site.register(CustomUser, CustomUserAdmin)
