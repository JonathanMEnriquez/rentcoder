# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# here
from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def landing_page(request):
    if Coder.objects.all().count() == 0:
        Coder.objects.create(first_name = 'Joe', alias = '2manygirlz', desc = "Hey. What’s up? My name is Joe (not my real name), aka 2manygirlz. I am a really funny guy but when it comes to coding I’m very serious…like Disneyland-during-rainstorms-serious. I can get you all the black belts you need to slay the laaaaydes. Hit me up!", email = 'laydasman@mail.com', age = 45, url_img = "https://i.ytimg.com/vi/3uFNiwrSqZA/maxresdefault.jpg")
        Coder.objects.create(first_name = 'Patrick', alias = 'boywonder', desc = "Greetings. More important than engaging in the social convention of sharing my given name, is the fact that I have an IQ of 182. I am eager to find something that occupies my time. Also, Mom doesn’t make me go outside for unnecessary physical exertion when I inform her that I am currently contracted for work. Please, hire me so that I don’t get picked on by the neighbor kids. Also, I need money to have enough seed money to launch my second start-up.  That, and for some fidget spinners and amiibos.", email = 'insideisbetterthanoutside@gmail.com', age = 10, url_img = "http://resize.indiatvnews.com/en/centered/newbucket/750_533/2016/05/mukund-soni-the-10-year-old-genius-1463485761.jpg")
        Coder.objects.create(first_name = 'Dmitry', alias = 'down_with_Putin23', desc = "Hello! My name is Dmitry, also known as down_with_Putin23. I like sushi and coding. Enough, please, do not make me choose what I like best, because it will be impossible for me to do it. I know that all the languages so hire me.", email = 'dmitrycodingmaster@gmail.com', age = 31, url_img = "https://2ch.hk/b/arch/2017-02-18/src/146992234/14874280958510.jpg")
        # CREATE THE 3 CODERS
    context = {
        # QUERY DATA NEEDED
    }
    return render(request, 'rentcoder/landing_page.html', context)

def logout(request):
    if 'cart' in request.session:
        cart = request.session['cart']
        request.session.clear()
        request.session['cart'] = cart
    else:
        request.session.clear()
    return redirect('/')

def register(request):
    if 'id' in request.session:
        return redirect('/dashboard/{}'.format(request.session['id']))
    return render(request, 'rentcoder/register.html')

def remove_user(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    User.objects.removeUser(user_id)
    return redirect('/home/admin')

def remove_coder(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    Coder.objects.removeCoder(coder_id)
    return redirect('/home/admin')

def remove_order(request, order_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    Order.objects.removeOrder(order_id)
    return redirect('/home/admin')

def order(request):
    try:
        request.session['id']
    except:
        return redirect('/')

    context = {
        'coders'    : Coder.objects.all()[:3] # ONLY 3 CODERS
    }
    return render(request, 'rentcoder/order.html', context)

def checkout(request):
    try:
        request.session['id']
    except:
        return redirect('/')

    request.session['cart'] = {
        'coder'     : request.POST['coder'],
        'exam'      : request.POST['exam_subject'],
        'date'      : request.POST['date']
    }
    return render(request, 'rentcoder/checkout_official.html', {'coder_name' : Coder.objects.get(id=request.POST['coder'])})

def charge(request):
    cart = request.session['cart']
    user_id = request.session['id']
    neworder = Order.objects.addOrder(cart, user_id)
    return redirect('/dashboard/'+str(request.session['id']))

def admin_home(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    context = {
        'user' : User.objects.get(id=request.session['id']),
        'all_users' : User.objects.all(),
        'all_coders': Coder.objects.all(),
        'all_orders': Order.objects.all()
    }
    return render(request, 'rentcoder/admin_home.html', context)

def admin_coders(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    context = {
        'user' : User.objects.get(id=request.session['id']),
        'all_coders' : Coder.objects.all()
    }
    return render(request, 'rentcoder/admin_coders.html', context)

def admin_orders(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    context = {
        'user' : User.objects.get(id=request.session['id']),
        'all_orders' : Order.objects.all()
    }
    return render(request, 'rentcoder/admin_orders.html', context)

def edit_user(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    context = {
        'user' : User.objects.get(id=user_id)
    }
    return render(request, 'rentcoder/admin_edit_user.html', context)

def edit_coder(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

    context = {
        'coder' : Coder.objects.get(id=coder_id)
    }
    return render(request, 'rentcoder/admin_edit_coder.html', context)

def edit_order(request, order_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))

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
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))
    # VALIDATE CHANGES?
    errors = User.objects.validateEditUser(request.POST,user_id)
    if errors:
        for message in errors['errors']:
            messages.error(request, message)
    else:
        User.objects.editUser(request.POST,user_id)
        messages.success(request, 'Succesfully Updated User')
    return redirect('/edit/user/{}'.format(user_id))

def edit_coder_process(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))
    # VALIDATE CHANGES?
    errors = Coder.objects.validateEditCoder(request.POST,coder_id)
    if errors:
        for message in errors['errors']:
            messages.error(request, message)
    else:
        Coder.objects.editCoder(request.POST,coder_id)
        messages.success(request, 'Succesfully Updated Coder')
    return redirect('/edit/coder/{}'.format(coder_id))

def edit_order_process(request, order_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard/'+str(request.session['id']))
    # VALIDATE CHANGES?
    errors = Order.objects.validateEditOrder(request.POST,order_id)
    if errors:
        for message in errors['errors']:
            messages.error(request, message)
    else:
        Order.objects.editOrder(request.POST,order_id)
        messages.success(request, 'Succesfully Updated Order')
    return redirect('/edit/order/{}'.format(order_id))

def process(request, action):
    if request.method == 'POST':
        if action == 'add':
            check_submission = User.objects.validateRegistration(request.POST)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    messages.error(request, message)
                return redirect('/register')
            else:
                newuser = User.objects.addUser(request.POST)
                if User.objects.all().count() == 1:
                    user_admin = User.objects.first()
                    user_admin.admin = True
                    user_admin.save()
                print newuser
                request.session['id'] = newuser.id
                return redirect('/dashboard/'+str(request.session['id']))
        elif action == 'login':
            if len(request.POST['user_input']) < 1 or len(request.POST['password']) < 8:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            user_id = User.objects.validateLogin(request.POST)
            if user_id:
                request.session['id'] = user_id
                return redirect('/dashboard/'+str(request.session['id']))
            else:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            return redirect('/')
    else:
        print 'get out of the main process'
        return redirect('/')

def dashboard(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    the_user = User.objects.get(id=request.session['id'])
    if request.session['id'] != int(user_id) and not the_user.admin:
        return redirect('/dashboard/'+str(request.session['id']))
    context = {
        'all_orders'   : Order.objects.filter(user=user_id),
        'user'          : User.objects.get(id=user_id),
        'user_messages': Message.objects.filter(addressee = user_id),
    }
    return render(request, 'rentcoder/dashboard.html', context)

def coder_profile(request, coder_id):
    try:
        request.session['id']
    except:
        return redirect('/')
    context = {
        'coder' : Coder.objects.get(id=coder_id)
    }
    return render(request, 'rentcoder/coder_profile.html', context)

# def admin_home(request):
#     return redirect('/home/admin/users')

def addmessage(request, user_id):
    if request.method == 'POST':
        try:
            creator = User.objects.get(id = request.session['id'])
            addressee = User.objects.get(id = user_id)
        except:
            return redirect('/dashboard/{}'.format(user_id))
        check_submission = Message.objects.validateMessage(request.POST)
        if len(check_submission) > 0:
            messages.error(request, check_submission['error'])
            return redirect('/dashboard/{}'.format(user_id))
        else:
            new_message = Message.objects.addMessage(request.POST, creator, addressee)
            return redirect('/dashboard/'+str(user_id))
    else:
        print 'get out of addmessage'
        return redirect('/dashboard/'+str(user_id))

def addcomment(request, user_id, message_id):
    if request.method == 'POST':
        try:
            creator = User.objects.get(id = request.session['id'])
            addressee = User.objects.get(id = user_id)
        except:
            return redirect('/dashboard/'+str(user_id))
        check_submission = Comment.objects.validateComment(request.POST)
        if len(check_submission) > 0:
            messages.error(request, check_submission['error'])
            return redirect('/dashboard/'+str(user_id))
        else:
            message = Message.objects.get(id = message_id)
            user = User.objects.get(id = request.session['id'])
            new_comment = Comment.objects.addComment(request.POST, user, message)
            return redirect('/dashboard/'+str(user_id))
    else:
        print 'get out of addcomment'
        return redirect('/dashboard/'+str(user_id))