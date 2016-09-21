from django import forms

from .models import User


class ProfileForm(forms.ModelForm):
    verified = forms.BooleanField(label='Email Verified', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['verified'].initial = self.instance.verified

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'city', 'state', 'institute']
