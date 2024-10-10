from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.forms import ModelForm
from .models import CV_Model, UploadedCV

class RegistrationForm(UserCreationForm):
        email = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email', 'style':'opacity:0.8'}))
        username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username', 'style':'opacity:0.8'}))
        password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'style':'opacity:0.8'}))
        password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password', 'style':'opacity:0.8'}))
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control', 'PlaceHolder':'Username', 'style':'opacity:0.8; color:black'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'class':'form-control', 'PlaceHolder':'Password', 'style':'opacity:0.8;'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email',
    'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))

class CVUploadForm(ModelForm):
    class Meta:
        model = CV_Model
        fields = ['cv_file']


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCV
        fields = ['cv_file']