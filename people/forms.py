from django import forms

from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'city', 'state', 'institute', 'verified']
