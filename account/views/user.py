from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings

from account.forms import RegistrationForm, LoginForm
from account.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password, backend='account.backends.EmailBackend')
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'account/registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = f'http://{domain}/accounts/activate/{uid}/{token}'
            subject = 'Activate your account'
            message = f'Click the link below to activate your account: {link}'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            messages.success(request, 'Account was successfully created. Check your email for activation link.')
            return redirect('account:login')

    else:
        form = RegistrationForm()
    return render(
        request,
        'account/registration/register.html', {'form': form}
    )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account was successfully activated.')
        return redirect('account:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('account:register')


def user_logout(request):
    logout(request)
    return redirect('account:login')