import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image

# Posting contents from other websites
"""
We will allow users to bookmark images from external websites and share them on our site
"""


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    # validation of url
    def clean_url(self):
        # The value of the url field is retrieved by accessing the cleaned_data dictionary of the form
        # instance
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        # The URL is split to check whether the file has a valid extension
        image_extension = url.rsplit('.', 1)[1].lower()
        if image_extension not in valid_extensions:
            raise forms.ValidationError("The given URL does not match valid image extensions")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        image_ext = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{image_ext}'
        # download image from the given URL
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()
        return image
