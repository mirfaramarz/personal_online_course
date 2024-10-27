from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.encoding import force_str 
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from .tokens import account_activation_token 



def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('base')  # Redirect to the home page if already logged in

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user using EmailBackEnd
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, 'Email and password are not valid!')
            return redirect('login')

    return render(request, 'registration/login.html')

ALLOWED_DOMAINS = [
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com',
    'icloud.com', 'mail.com', 'protonmail.com', 'zoho.com', 'gmx.com',
    'yandex.com', 'comcast.net', 'att.net', 'verizon.net', 'sbcglobal.net',
    'msn.com', 'live.com', 'me.com', 'mac.com', 'qq.com', 'baidu.com',
    'naver.com', 'hanmail.net', 'daum.net', 't-online.de', 'web.de',
    'bluewin.ch', 'orange.fr', 'wanadoo.fr', 'free.fr', 'virginmedia.com',
    'btinternet.com', 'sky.com', 'talktalk.net', 'ntlworld.com', 'cox.net',
    'earthlink.net', 'optonline.net', 'bellsouth.net'
]

def register(request):
    if request.user.is_authenticated:
        return redirect('base')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email is from an allowed domain
        email_domain = email.split('@')[-1]  # Extract the domain from email
        if email_domain not in ALLOWED_DOMAINS:
            messages.warning(request, 'Email domain is not allowed. Please use a valid domain.')
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists.')
            return redirect('register')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists.')
            return redirect('register')

        # Create the user and set as inactive until email confirmation
        user = User(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        # Send confirmation email
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://{request.get_host()}/accounts/activate/{uid}/{token}/"
        
        subject = 'Activate your account'
        message = 'Please confirm your email by clicking the link below.'
        html_message = render_to_string('registration/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
        )

        messages.success(request, 'Please confirm your email address to complete the registration.')
        return redirect('login')

    return render(request, 'registration/register.html')
        
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Use force_str instead of force_text
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # Activate the user account
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('base') 


def profile(request):
    return render(request, 'registration/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password !=None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile has been successfuly updated.')
        return redirect('profile')