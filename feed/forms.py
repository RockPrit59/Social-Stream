from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # NEW: Add 'image' to the list of fields
        fields = ['content', 'image']
        
        labels = {'content': '', 'image': ''}
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "What's on your mind?"}),
            # Add styling for the file upload button too
            'image': forms.FileInput(attrs={'class': 'form-control mt-2'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Write a comment..."}),
        }