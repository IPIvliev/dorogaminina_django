from django import forms

class SignUpForm(forms.Form):
  lastname = forms.CharField(widget=forms.TextInput(attrs={"class":"span4", 'placeholder': 'Фамилия'}), label="", required=True)
  name = forms.CharField(widget=forms.TextInput(attrs={"class":"span4", 'placeholder': 'Имя'}), label="", required=True)
  otchestvo = forms.CharField(widget=forms.TextInput(attrs={"class":"span4", 'placeholder': 'Отчество'}), label="")
  phone = forms.CharField(widget=forms.TextInput(attrs={"class":"span12", 'placeholder': 'Номер телефона'}), label="", required=True)

class LoginForm(forms.Form):
  id = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"span3", 'placeholder': 'Ваш ID'}), label="", required=True)
  password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"span4", 'placeholder': 'Пароль из sms'}), label="", required=True)
