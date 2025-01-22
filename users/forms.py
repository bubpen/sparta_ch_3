from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', )