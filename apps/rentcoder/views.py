# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def index(request):
    return render(request, 'rentcoder/index.html')

def register(request):
    return render(request, 'rentcoder/register.html')

def process(request, action):
    if request.method == 'POST':
        if action == 'add':
            check_submission = User.objects.validateRegistration(request.POST)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    messages.error(request, message)
                return redirect('/')
            else:
                newuser = User.objects.addUser(request.POST)
                print newuser
                request.session['id'] = newuser.id
                return redirect('/home')
        elif action == 'login':
            if len(request.POST['user_input']) < 1 or len(request.POST['password']) < 8:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            user = User.objects.validateLogin(request.POST)
            if user:
                request.session['id'] = user
                return redirect('/home')
            else:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            return redirect('/')
    else:
        print 'get out of the main process'
        return redirect('/')

def home(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    the_user = User.objects.get(id=request.session['id'])
    return render(request, 'rentcoder/welcome.html', {'user': the_user})