# challenges/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields to include in the form

# challenges/forms.py


from django import forms
from .models import Submission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code', 'language', 'problem']
        widgets = {
            'code': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'language': forms.Select(choices=[('python', 'Python'), ('java', 'Java'), ('c', 'C'), ...]),
        }
