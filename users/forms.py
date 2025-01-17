from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)