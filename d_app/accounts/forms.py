from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Acme Inc. (optional)'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'company', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'your_username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            from accounts.models import UserProfile
            UserProfile.objects.create(
                user=user,
                company=self.cleaned_data.get('company', '') or '',
                plan='free'
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your_username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
