from django import forms
from django.conf import settings


class ImportForm(forms.Form):
    file = forms.FileField()
    tag_name = forms.CharField(max_length=settings.MODEL_TAG_NAME_MAX_LEN)
