from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth import login,logout
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required 
# Create your views here.

def search(one,two,three,four,five,id):
    all = History.objects.all()
    temp = []
    for it in all:
        if it.id != id:
            if it.one == one or it.one == two or it.one == three or it.one == four or it.one == five:
                temp.append(it)
                continue
            elif it.two == one or it.two == two or it.two == three or it.two == four or it.two == five:
                temp.append(it)
                continue
            elif it.three == one or it.three == two or it.three == three or it.three == four or it.three == five:
                temp.append(it)
                continue
            elif it.four == one or it.four == two or it.four == three or it.four == four or it.four == five:
                temp.append(it)
                continue
            elif it.five == one or it.five == two or it.five == three or it.five == four or it.five == five:
                temp.append(it)
                continue
    if temp != None:
        return temp
    else:
        return None


def index(request):
    headtitle = "Let's Match | Home"
    user = request.user
    find = []
    if user.is_authenticated:
        try:
            history = History.objects.get(id=user)
        except ObjectDoesNotExist:
            history = None
        if history != None:
            send_mail(
                    'You found a Match!',
                    'Login Now, letsmatch.pythonanywhere.com to check your Match',
                    'ekesel05@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
            res = search(history.one,history.two,history.three,history.four,history.five,history.id)
            if res != None:
                find = res
            else:
                find = res
        if request.method == 'POST':
            instaid = request.POST['instaid']
            mobno = request.POST['mobno']
            one = request.POST['one']
            two = request.POST['two']
            three = request.POST['three']
            four = request.POST['four']
            five = request.POST['five']
            if history == None:
                History.objects.create(id=user,instaid=instaid,mobno=mobno,one=one,two=two,three=three,four=four,five=five)
                messages.success(request,"Sucessfully Submitted! We will mail you when you get a match!")
                return redirect('index')
            else:
                History(id=user,instaid=instaid,mobno=mobno,one=one,two=two,three=three,four=four,five=five).save()
                messages.success(request,"Sucessfully Submitted! We will mail you when you get a match!")
                return redirect('index')
        
        parms = {
            'headtitle': headtitle,
            'find': find,
            'history':history,
            'user':user,
        }
        return render(request, 'index.html', parms)
    else:
        return redirect('register')
    
    return render(request, 'index.html', {'headtitle':headtitle,})


def contact(request):
    headtitle = "Let's Match | Contact"
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['message']
        Contact(email=email,message=message).save()
        messages.success(request,"Sucessfully Submitted! We will mail you when you get a match!")

    return render(request,'contact.html',{'headtitle':headtitle,})

def register(request):
    head = "Let's Match | REGISTER"
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email).save()
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request,'Check email and Verify your account')
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('register')
    return render(request,'signup.html',{'head':head})

def login(request):
    head = "Let's Match | LOGIN"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,'Logged In Successfully')
            return redirect('index')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html',{'head':head})

def logouts(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')