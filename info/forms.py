from info.models import *
from django import forms


class CotnactForm(forms.ModelForm):
    class Meta:
        model = ContactUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'messages']
