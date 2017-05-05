from django import forms


class SignUpForm(forms.Form):
    fname = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lname = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    address = forms.CharField(required=True,max_length=200, widget=forms.Textarea(attrs={'placeholder': 'Address','rows':5, 'cols':20}))
    username = forms.CharField(required=True,max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True,max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True,max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


