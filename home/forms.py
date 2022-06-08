from django import forms
from home.models import User

class SignUpForm(forms.ModelForm):
  lastname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Фамилия'}), label="", required=True)
  username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Имя'}), label="", required=True)
  middlename = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Отчество'}), label="")
  phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "id": "phone", 'placeholder': 'Номер телефона'}), label="", required=True)

  class Meta: 
    model = User 
    fields =('username', 'lastname', 'middlename', 'phone') 

class LoginForm(forms.Form):
  phone = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control", 'placeholder': 'Ваш Номер телефона'}), label="", required=True)
  password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", 'placeholder': 'Пароль из sms'}), label="", required=True)
  
  class Meta: 
    model = User 
    fields =('phone', 'password') 