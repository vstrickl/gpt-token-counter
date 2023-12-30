import os

from django.conf import settings
from django import forms

# Create your forms here.
class SplitTextForm(forms.Form):
    file_name = forms.CharField(label='File Name', max_length=100, required=False)
    tokens_per_file = forms.IntegerField(label='Tokens Per File', initial=2200, required=False)
    file = forms.FileField(label='Upload File', required=False)
    existing_file = forms.ChoiceField(label='Or Select Existing File', required=False)

    def __init__(self, *args, **kwargs):
        super(SplitTextForm, self).__init__(*args, **kwargs)
        self.fields['existing_file'].choices = self.get_existing_files()

    def get_existing_files(self):
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(uploads_dir):
            return []

        files = [(os.path.join(uploads_dir, f), f) for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
        return [('', '--- Select a File ---')] + files

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload File', required=False)
    existing_file = forms.ChoiceField(label='Or Select Existing File', required=False)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['existing_file'].choices = self.get_existing_files()

    def get_existing_files(self):
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(uploads_dir):
            return []

        files = [(os.path.join(uploads_dir, f), f) for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
        return [('', '--- Select a File ---')] + files