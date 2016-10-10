from django import forms


class TeamForm(forms.Form):
    name = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
