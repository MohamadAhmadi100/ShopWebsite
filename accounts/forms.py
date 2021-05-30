from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("گذرواژه ها مطابقت ندارند")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username')


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=50, label='ایمیل',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, label='رمز عبور',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(max_length=50, label='ایمیل',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, label='نام کاربری',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, label='رمز عبور',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, label='تایید رمز عبور',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("گذرواژه ها مطابقت ندارند")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("کاربری با ایمیل وارد شده وجود دارد")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError("کاربری با نام کاربری وارد شده وجود دارد")
        return username
