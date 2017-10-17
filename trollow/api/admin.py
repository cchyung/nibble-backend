from __future__ import unicode_literals
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):

    class Meta():
        model = User
        fields = ('email', 'password',)

class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )

admin.site.register(User, UserAdmin)
