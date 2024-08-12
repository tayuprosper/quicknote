from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Note(models.Model):
    notesContent = models.TextField(max_length=1024)
    date_created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=50)
    is_fav = models.BooleanField(default=False)
    def __str__(self):
        return self.note_title
    