from __future__ import unicode_literals
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class UserCreateForm(UserCreationForm):

    class Meta():
        model = User
        fields = ('email', 'password',)

class UserAdmin(UserAdmin):
    add_form = UserCreateForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Truck)
admin.site.register(Post)
admin.site.register(LikedTruck)
admin.site.register(TruckRating)
admin.site.register(MenuItem)
