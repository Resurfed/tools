from django import forms
from django.utils.safestring import mark_safe

from .models import Server
from .choices import MapTypeChoices


class UploadForm(forms.Form):

    insert_map_info = forms.BooleanField(
        initial=False,
        help_text="Insert map info on upload",
        required=False
    )

    map_author = forms.CharField(
        max_length=32,
        help_text="Map Author",
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '[pfN] big blue',
                'class': '',
                'tabindex': 2,
                'disabled': True,
            }
        )
    )

    map_type = forms.ChoiceField(
        choices=MapTypeChoices,
        required=False,
        help_text="Map Type",
        widget=forms.Select(
            attrs={
                'placeholder': 1,
                'tabindex': 3,
                'disabled': True
            }
        )
    )

    map_tier = forms.IntegerField(
        min_value=1,
        max_value=6,
        help_text="Tier of the map, choose carefully!",
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 4,
                'disabled': True
            }
        )
    )

    map_zones = forms.IntegerField(
        min_value=1,
        max_value=32,
        help_text=mark_safe("Staged maps = Stages <br/> Linear maps = checkpoints + 1 <br/> "
                            "Linear maps must have at least 1 checkpoint!"),
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 5,
                'disabled': True,
                'size': 10
            }
        )
    )

    map_bonuses = forms.IntegerField(
        min_value=1,
        max_value=32,
        help_text="Number of bonuses",
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 6,
                'disabled': True
            }
        )
    )

    map_disable_pre_hop = forms.BooleanField(
        initial=False,
        required=False,
        help_text="Disable prehopping"
    )

    map_enable_baked_triggers = forms.BooleanField(
        initial=False,
        required=False,
        help_text="Enabled baked in triggers"
    )

    map_spawns = forms.CharField(
        required=False,
        help_text=mark_safe("Format: type:zone:pos:ang <br/>"
                            "types - map, stage, bonus <br/>"
                            "zone - use the matching stage or bonus number <br/>"
                            "pos - the pos coordinates from getpos (No decimals)<br/>"
                            "ang - the ang coordinates from getang (No decimals)<br/>"
                            "Note: For the map spawn leave the zone parameter empty! <br/>"),
        widget=forms.Textarea(
            attrs={
                'placeholder': mark_safe('stage:1:100,200,300:0,90,0\n'
                                         'bonus:5:100,200,300:0,90,0\n'
                                         'map::100,200,300:0,90,0'),
                'class': '',
                'tabindex': 9,
                'disabled': True
            }
        )
    )

    servers = forms.ModelMultipleChoiceField(
        queryset=Server.objects.none(),
        required=False,
        help_text="Servers",
        widget=forms.SelectMultiple(
            attrs={
                'class': 'ui fluid search servers dropdown',
                'tabindex': 10
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['servers'].queryset = Server.objects.all()