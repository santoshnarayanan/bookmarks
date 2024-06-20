from django import forms
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
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL does not match valid image extensions")
        return url
