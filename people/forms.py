from django import forms

from .models import User, Contestant


class ProfileForm(forms.ModelForm):
    verified = forms.BooleanField(label='Email Verified', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['verified'].initial = self.instance.verified

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'city', 'state', 'institute']


class HackerrankForm(forms.ModelForm):

    class Meta:
        model = Contestant
        fields = ['hackerrank']

    def is_valid(self, **kwargs):

        # run the parent validation first
        valid = super().is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        hr = kwargs.get('hackerrank')
        if hr != self.cleaned_data['hackerrank'] and Contestant.objects.filter(hackerrank=self.cleaned_data['hackerrank']).exists():
            self._errors['hackerrank'] = 'Another account is already registered with this HackerRank username.' \
                                              'Please contact HashInclude if you have any issues.'
            return False
        return True
