from django import forms

class VideoUrlForm(forms.Form):
    url = forms.URLField(label="YouTube Video URL", widget=forms.URLInput(attrs={'placeholder': 'Enter YouTube URL'}))
    format_choice = forms.ChoiceField(label="Choose Format", widget=forms.Select)
