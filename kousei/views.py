from django.shortcuts import render,redirect
from .forms import KouseiForm,RegistrationForm,LoginForm,SentenceForm
from django.http import HttpResponse
from urllib import request, parse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from . import api

def kousei(request):
    params = {
            'status':'',
            'kekka':'',
            'score':'',
            'form':KouseiForm(),
        }
    API = api.Kousei()
    if (request.method == 'POST'):
        params['status'] = str(API.get(request)[0])
        params['kekka'] = str(API.get(request)[1])
        params['score'] = str(API.get(request)[2])
    return render(request,'kousei/kousei.html', params)

def sentence(request):
    params = {
            'messages':'',
            'error':'',
            'form':SentenceForm(),
        }
    API = api.Sentence()
    if (request.method == 'POST'):
        params['form'] = SentenceForm(request.POST)
        if API.get(request)==[]:
            params['error'] = '問題なし！'
        else:
            params['messages'] = API.get(request)
    return render(request,'kousei/sentence.html', params)

def register(request):
    if (request.method == 'POST'):
        try:
            registration_form = RegistrationForm(request.POST)
            ID = request.POST['ID']
            password = request.POST['password']
            user = User.objects.create_user(username=request.POST['ID'], password=password)
            params ={
                'registration_form': registration_form,
                'message':'登録完了しました！',
                'ID':'ID：'+ID,
                'password':'パスワード：'+password,
            }
            return render(request, 'kousei/register.html', params)
        except :
            registration_form = RegistrationForm()
            message = 'すでに登録されています！'
            return render(request, 'kousei/register.html', {'registration_form':registration_form,'message':message})
    else:
        registration_form = RegistrationForm()
        return render(request, 'kousei/register.html', {'registration_form': registration_form})

def login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        ID = request.POST['ID']
        password = request.POST['password']
        user = authenticate(request, username=ID, password=password)
        if user is not None:
            django_login(request, user)
            return render(request,'kousei/kousei.html',{'form':KouseiForm()})
        else:
            login_form.add_error(None, "IDまたはパスワードが違います！")
            return render(request, 'kousei/login.html', {'login_form': login_form})
        return render(request, 'kousei/login.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
    return render(request, 'kousei/login.html', {'login_form': login_form})

