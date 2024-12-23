from django import forms

from .models import Dweet, Comment

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user", "likes")  # 排除'user'和'likes'字段

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Add a comment...",
                "class": "textarea is-small",
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        exclude = ("user", "dweet")
