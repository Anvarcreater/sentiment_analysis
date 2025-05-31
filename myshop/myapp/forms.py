from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate

class SignupForm(forms.ModelForm):
    username=forms.CharField(label="Username",max_length=100,required=True)
    email=forms.EmailField(label="Email",max_length=100,required=True)
    password=forms.CharField(label="Password",max_length=100,required=True)

    class Meta:
        model=User
        fields=['username','email','password']

class LoginForm(forms.Form):
    username=forms.CharField(label="username",max_length=100,required=True)
    password=forms.CharField(label="password",max_length=100,required=True)

    def clean(self):
        cleaned_data=super().clean()
        username=cleaned_data.get("username")
        password=cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("invalid email or password")
            
class ForgotForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=100,required=True)

    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("no user found ! Enter a correct email id  ")
        
class ResetPasswordForm(forms.Form):
    new_password=forms.CharField(label="new_password",max_length=100,required=True)
    confirm_password=forms.CharField(label="confirm_password",max_length=100,required=True)

    def clean(self):
        cleaned_data=super().clean()
        new_password=cleaned_data.get("new_password")
        confirm_password=cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password!=confirm_password:
            raise forms.ValidationError("password mismatched...!")



