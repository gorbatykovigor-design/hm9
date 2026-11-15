
from django import forms
from django.core.exceptions import ValidationError
from .models import Comment
import re


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']

        if re.search(r'<[^>]*>', text):
            raise ValidationError("HTML-теги заборонені!")

        if len(text) > 500:
            raise ValidationError("Максимум 500 символів!")

        return text
