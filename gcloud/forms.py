from django import forms

# Create your Forms here.
class UserQuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea, label='Ask your question')