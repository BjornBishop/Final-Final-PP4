from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment, ContactMessage
import re

# forum models go below here

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'industry', 'duration', 'rate', 'currency', 'requirements', 'description']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        # Check for email patterns
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Check for phone number patterns
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if re.search(email_pattern, description) or re.search(phone_pattern, description):
            raise forms.ValidationError("Contact information is not allowed in the description")
        return description

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)

