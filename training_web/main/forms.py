from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class EditProfileForm(ModelForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

