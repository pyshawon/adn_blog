from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from django.contrib.auth import (
    authenticate, 
    get_user_model
)

# assign User to User model using get_user_model() 
User = get_user_model()

class UserLoginForm(forms.Form):
    """
    User Login form with email and password field.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        # if email not provided raise ValidationError
        data = self.cleaned_data['email']
        if not data:
            raise forms.ValidationError("Please enter email")
        return data

    def clean_password(self):
        # if password not provided raise ValidationError
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError("Please enter your password")
        return data


    def clean(self):
        """
        Authenticate user with Email & password.
        Raise ValidationError if user is inactive or wrong username or password.
        """
        super(UserLoginForm, self).clean()
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            user_exists = User.objects.filter(email=email).last()
            if user_exists and not user_exists.is_active:
                raise forms.ValidationError("Inactive User")
            else:
                raise forms.ValidationError("Invalid Username or Password")
            
        return self.cleaned_data




def UniqueEmailValidator(value):
    """
    A Custom Unique Email Validator.
    """
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists.')

class UserRegisterForm(forms.ModelForm):
    """
    User Register form.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password'
        ]

        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Init UniqueEmailValidator.
        self.fields['email'].validators.append(UniqueEmailValidator)

    def clean_password(self):
        # if password not provided raise ValidationError
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError("Please enter your password")
        return data

    def clean_confirm_password(self):
        # if confirm_password not provided raise ValidationError
        data = self.cleaned_data['confirm_password']
        if not data:
            raise forms.ValidationError("Please enter your confirm password")
        return data
    
    def clean_email(self):
        # if email not provided raise ValidationError
        data = self.cleaned_data.get('email')
        if not data:
            raise forms.ValidationError("Please enter your email")
        return data

    def clean(self):
        """
        Check password & confirm_password is matched or not.
        """        
        super(UserRegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and password != confirm_password:
            raise forms.ValidationError("password must match")
        return self.cleaned_data





