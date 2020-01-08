from django import forms
from .models import Comment
from captcha.fields import ReCaptchaField 
from captcha.widgets import ReCaptchaV2Checkbox

class CommentForm(forms.ModelForm):
    """ Implements a form for a comment """
    class Meta:
        model = Comment 
        fields = ('name','email','body')
        forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'placeholder': 'Search for...'}))