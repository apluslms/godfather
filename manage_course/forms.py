from django.forms import ModelForm
from manage_course.models import CourseRepository
from django import forms

class RepoForm(ModelForm):
    class Meta:
        model = CourseRepository
        fields = ['key', 'git_origin', 'git_branch', 'name', 'owner']

    key = forms.SlugField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
