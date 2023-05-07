from django import forms
from captcha.fields import CaptchaField
from events.models import Merch, Place, Order, Message

class MerchModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % (obj.size)

class PlaceModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
        free_palce = obj.amount - obj.busy
        return "%s свободно мест: %i" % (obj.place_name, free_palce)

class FinalOrderForm(forms.Form):
  order_merch = MerchModelChoiceField(queryset=Merch.objects.all(), label="Выберите размел футболки", widget=forms.Select(attrs={'class':'form-control'}))
  order_place = PlaceModelChoiceField(queryset=Place.objects.all(), label="Выберите звено", widget=forms.Select(attrs={'class':'form-control'}))
  #order_place = forms.CharField(widget=forms.ChoiceField(attrs={"class":"form-control", 'placeholder': 'Пароль из sms'}), label="", required=True)
  comment = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", 'placeholder': 'Комментарий до 250 символов'}), label="", required=False)
  
  class Meta: 
    model = Order 
    fields =('order_place', 'order_merch', 'comment')
  
  def __init__(self, *args, **kwargs):
    event = kwargs.pop('event', None)
    order = kwargs.pop('order', None)
    #self.fields['order_merch'].widget.attrs = {"class":"form-control"}
    super(FinalOrderForm, self).__init__(*args, **kwargs)

    if event:
      self.fields['order_merch'].queryset = Merch.objects.filter(merch_event=event, active=True)
      if order.price == 1500:
        self.fields['order_place'].queryset = Place.objects.filter(place_event=event, free__gt=0, active=True, place_name__iregex=r"^((?!Балахна).)*$")
      else:
        self.fields['order_place'].queryset = Place.objects.filter(place_event=event, free__gt=0, active=True, place_name__iregex=r"Балахна")

class MessageForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Имя'}), label="", required=True)
  email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Email'}), label="", required=True)
  captcha = CaptchaField()
  message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", 'placeholder': 'Сообщение до 1000 символов'}), label="", required=True)

  class Meta: 
    model = Message
    fields =('name', 'email', 'message')