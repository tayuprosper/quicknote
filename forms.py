from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, User
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["note_title", "notesContent"]

class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email","password"]

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None  # Set help_text to None

    class Meta:
        model = User
        fields = ["username","first_name", "last_name","password1","password2"]
       