from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from additional_user.models import Profile


class ProfileInlineForm(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class SystemUser(admin.ModelAdmin):
    inlines = [
        ProfileInlineForm
    ]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(SystemUser, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, SystemUser)

# if error on login
# from django.contrib.auth.models import User
# from additional_user.models import Profile
# for user in User.objects.all():
#     Profile.objects.get_or_create(user=user)