from django import forms

# Create your forms here.
class SplitTextForm(forms.Form):
    file = forms.FileField(label='Upload File')
    tokens_per_file = forms.IntegerField(label='Tokens Per File', initial=2200, required=False)
    file_name = forms.CharField(label='File Name', max_length=100, required=False)