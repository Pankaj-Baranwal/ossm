from django import forms

from events.models import Team, Event


class TeamForm(forms.ModelForm):
    event = forms.ModelChoiceField(Event.objects.filter(max_team_size__gt=1).all(), empty_label='(Nothing)')

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if 'instance' in kwargs:
            self.fields['event'].initial = kwargs.get('instance').event

    class Meta:
        model = Team
        fields = ['nickname', 'name', 'second_member']
