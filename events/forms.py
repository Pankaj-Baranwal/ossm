from django import forms

from events.models import Team, Event


class TeamForm(forms.ModelForm):
    event = forms.ModelChoiceField(Event.objects.filter(max_team_size__gt=1).all(), empty_label='(Nothing)')

    class Meta:
        model = Team
        fields = ['nickname', 'name', 'second_member']
