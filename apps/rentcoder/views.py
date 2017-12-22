# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# here
from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def index(request):
    if Coder.objects.all().count() == 0:
        Coder.objects.create(first_name = 'Joe', alias = '2manygirlz', desc = "Hey. What’s up? My name is Joe (not my real name), aka 2manygirlz. I am a really funny guy but when it comes to coding I’m very serious…like Disneyland-during-rainstorms-serious. I can get you all the black belts you need to slay the laaaaydes. Hit me up!", email = 'laydasman@mail.com', age = 45, url_img = "https://i.ytimg.com/vi/3uFNiwrSqZA/maxresdefault.jpg")
        Coder.objects.create(first_name = 'Dmitry', alias = 'down_with_Putin23', desc = "Hello! My name is Dmitry, also known as down_with_Putin23. I like the sushi and the coding. Enough, please, do not make me choose what I like best, because it will be impossible for me to do it. I know that all the languages and platforms they teach it in your Dojo Coding hire me to help you get job in your land of freedom. :)", email = 'dmitrycodingmaster@gmail.com', age = 31, url_img = "https://2ch.hk/b/arch/2017-02-18/src/146992234/14874280958510.jpg")
        Coder.objects.create(first_name = 'Patrick', alias = 'boywonder', desc = "Greetings. More important than engaging in the social convention of sharing my given name, is the fact that I have an IQ of 182. I am eager to find something that occupies my time. Also, Mom doesn’t make me go outside for unnecessary physical exertion when I inform her that I am currently contracted for work. Please, hire me so that I don’t get picked on by the neighbor kids. Also, I need money to have enough seed money to launch my second start-up.  That, and for some fidget spinners and amiibos.", email = 'insideisbetterthanoutside@gmail.com', age = 10, url_img = "http://resize.indiatvnews.com/en/centered/newbucket/750_533/2016/05/mukund-soni-the-10-year-old-genius-1463485761.jpg")
        # CREATE THE 3 CODERS
    context = {
        # QUERY DATA NEEDED
    }
    return render(request, 'rentcoder/landing_page.html', context)

def login(request):
    return render(request, 'rentcoder/login.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    return render(request, 'rentcoder/register.html')

def order(request):
    context = {
        'coders'    : Coder.objects.all()[:3] # ONLY 3 CODERS
    }
    return render(request, 'rentcoder/order.html', context)

def checkout(request):
    return HttpResponse("checkout page ~ idk stripe yet")

def admin_users(request):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'rentcoder/admin_home.html', context)

def admin_coders(request):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')
    context = {
        'coders' : Coder.objects.all()
    }
    return render(request, 'rentcoder/admin_coders.html', context)

def admin_orders(request):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')
    context = {
        'orders' : Order.objects.all()
    }
    return render(request, 'rentcoder/admin_orders.html', context)

def edit_user(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')

    context = {
        'user' : User.objects.get(id=user_id)
    }
    return render(request, 'rentcoder/admin_edit_user.html')

def edit_coder(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')

    context = {
        'coder' : Coder.objects.get(id=coder_id)
    }
    return render(request, 'rentcoder/admin_edit_coder.html')

def edit_order(request, order_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')

    context = {
        'order' : Order.objects.get(id=order_id),
        'all_users' : User.objects.all(),
        'all_coders': Coder.objects.all()
    }
    return render(request, 'rentcoder/admin_edit_order.html', context)

def edit_user_process(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/{}'.format(request.session['id']))
    # VALIDATE CHANGES
    return redirect('/')

def edit_coder_process(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/{}'.format(request.session['id']))
    # VALIDATE CHANGES
    return redirect('/')

def edit_order_process(request order_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/{}'.format(request.session['id']))
    # VALIDATE CHANGES
    return redirect('/')

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
                if User.objects.all().count() == 1:
                    User.objects.first().admin = True

                print newuser
                request.session['id'] = newuser.id
                return redirect('/home')
        elif action == 'login':
            if len(request.POST['user_input']) < 1 or len(request.POST['password']) < 8:
                messages.warning(request, 'Invalid login information')
                return redirect('/login')
            user = User.objects.validateLogin(request.POST)
            if user:
                request.session['id'] = user
                return redirect('/home')
            else:
                messages.warning(request, 'Invalid login information')
                return redirect('/login')
            return redirect('/login')
    else:
        print 'get out of the main process'
        return redirect('/')

def dashboard(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    the_user = User.objects.get(id=request.session['id'])
    if request.session['id'] != user_id and not the_user.admin):
        return redirect('/dashboard/{}'.format(user_id))
    context = {
        'user_orders'   : Order.objects.filter(user=the_user)
    }
    return render(request, 'rentcoder/dashboard.html', context)

def coder_profile(request, coder_id):
    context = {
        'coder' : Coder.objects.get(id=coder_id)
    }
    return render(request, 'rentcoder/coder_profile.html', context)

def admin_home(request):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')
    elif checkuser.admin:
        context = {
            'user':User.objects.get(id = request.session['id']),
            'all_users': User.objects.exclude(id = request.session['id']).order_by('first_name'),
        }
        return render(request, 'rentcoder/admin_home.html', context)