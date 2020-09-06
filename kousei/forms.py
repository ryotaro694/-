from django import forms
import re

class KouseiForm(forms.Form):
    bunsyo = forms.CharField(label='文章を入力', max_length=500,min_length=50,\
        widget = forms.Textarea(attrs={'class':'form-control'}))
    
    data = [
        ('low','low'),
        ('medium','medium'),
        ('high','high'),
    ]

    sensivity = forms.ChoiceField(label='sensivity',\
        choices = data)

class LoginForm(forms.Form):
    ID = forms.CharField(label='ID', \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', min_length=8, \
        widget = forms.TextInput(attrs={'class':'form-control'}))

class RegistrationForm(forms.Form):
    ID = forms.CharField(label='ID', min_length=8, \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', min_length=8, \
        widget = forms.TextInput(attrs={'class':'form-control'}))

class SentenceForm(forms.Form):
    sentence = forms.CharField(label='文章を入力', max_length=500,min_length=10,\
        widget = forms.Textarea(attrs={'class':'form-control'}))

    data_1 = [
        ('1','表記、表現ミス'),
        ('2','わかりやすい表記'),
        ('3','文章の精度UP'),
    ]

    filter_group = forms.ChoiceField(label='filter_group',\
        choices = data_1)