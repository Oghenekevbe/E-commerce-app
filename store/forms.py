from django import forms
from .models import Customer, BillingAddress, Categories, Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
import secrets


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}), required=True)
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}), required=True)

    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        # Create a customer for the new user and assign the email confirmation token
        customer = Customer.objects.create(user=user)
        customer.email_confirmation_token = secrets.token_urlsafe()
        customer.save()

        return user


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


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

    def send_email(self):
        # Get the cleaned data from the form
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        # Construct the email message
        email_body = f"Name: {name}\nEmail: {email}\n\nMessage: {message}"
        email = EmailMessage(subject, email_body, to=[settings.EMAIL_HOST_USER])

        # Send the email
        email.send()





class AddAddressForm(forms.ModelForm):
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    state = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    zipcode = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
 
    class Meta:
        
        model = BillingAddress
        fields = ("address", "city", "state", "zipcode")



class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput( attrs={'class':'form-control'}), required=True)
    class Meta:
        model = Categories
        fields = ('name',)


choices = Categories.objects.all().values_list('name','name')
choice_list = []

for item in choices:
    choice_list.append(item)
    
digital_choices = [
    (True, 'Yes'),
    (False, 'No')
]
    
class ProductForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    category = forms.ChoiceField(choices=choice_list, widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    digital = forms.ChoiceField(choices=digital_choices, widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Product
        fields = ("image", "name", "description", "price", "digital", "category")

