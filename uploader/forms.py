from django import forms
from django.utils.safestring import mark_safe

from .models import Server, Database
from .choices import MapTypeChoices, ServerType, DatabaseType


class UploadForm(forms.Form):

    insert_map_info = forms.BooleanField(
        initial=False,
        help_text="Insert map info on upload",
        required=False
    )

    database = forms.ModelChoiceField(
        queryset=Database.objects.none(),
        required=False,
        help_text="Server to add the map to",
        widget=forms.Select(
            attrs={
                'disabled': True,
            }
        )
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

        servers = Server.objects
        databases = Database.objects

        if user.has_perm('uploader.uploader_admin'):
            servers = servers.all()
            databases = databases.all()
        else:
            servers = servers.filter(type__in=[ServerType.SERVER_PUBLIC]).all()
            databases = databases.filter(type__in=[DatabaseType.Public]).all()

        self.fields['servers'].queryset = servers
        self.fields['database'].queryset = databases