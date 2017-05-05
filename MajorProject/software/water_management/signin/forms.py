from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(required=True,max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True,max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


