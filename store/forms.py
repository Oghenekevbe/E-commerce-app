from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}), required=True)
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}), required=True)

    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        customer = Customer.objects.create(user=user)
        return customer


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})
        self.fields['password'].widget.attrs.update({'autocomplete': 'current-password'})

    def clean_username(self):
        email = self.cleaned_data.get('email')
        if email:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
            else:
                return user.username
        else:
            return self.cleaned_data.get('username')
        
        
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)

    
    class Meta:
        model = User
        fields = ("username","email")

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    new_password1 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    new_password2 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


