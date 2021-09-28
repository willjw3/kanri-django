from django import forms
from django.forms import widgets
from .models import Board, Task, Comment

class BoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('name', 'about', 'status')
    

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task 
        fields = ('title', 'content', 'label', 'assigned_to', 'status')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }
    
    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)