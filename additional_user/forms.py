from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

from additional_user.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

