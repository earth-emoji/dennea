from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Customer
from users.models import User

class CustomerSignUpForm(UserCreationForm):
    company_name = forms.CharField(min_length=1, max_length=30, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Company Name'}))
    email = forms.CharField(min_length=1, max_length=60, widget=forms.EmailInput(attrs={'class': '', 'placeholder': 'Email'}))
    name = forms.CharField(min_length=1, max_length=60, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Name'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': ''}))
    password1 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': '', 'placeholder': 'Password'}))
    password2 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': '', 'placeholder': 'Confirm Password'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('company_name', 'name', 'email', 'photo')

    # @transaction.atomic
    def save(self):
        user = super().save()
        Customer.objects.create(user=user)
        return user