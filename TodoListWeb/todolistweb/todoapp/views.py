from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password
# from django.views.generic import View, TemplateView, CreateView
# from django.contrib import messages
# from django.contrib.auth.tokens import default_token_generator
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'todoapp/index.html')

# Signup
def signupuser(request):
    if request.method == 'GET':
        form = UserSignUpForm()
    else:
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('todoapp/activate_account.html',
                                       {
                                           'user':user,
                                           'domain':current_site.domain,
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':account_activation_token.make_token(user),
                                        }
                                       )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject,message,to=[to_email])
            email.send()
            return HttpResponse('we have sent you an email')
    return render(request,'todoapp/signup.html',{'form':form})

    # if request.method == 'GET':
    #     return render(request, 'todoapp/signup.html')
    # elif request.method == 'POST':
    #     username = request.POST.get('username', None)
    #     email = request.POST.get('email',None)
    #     password = request.POST.get('password', None)
    #     password_confirm = request.POST.get('password_confirm', None)
    #
    #     res_data = {}
    #     if not(username and password and password_confirm):
    #         res_data['error'] = '모든 값을 입력해야합니다. 다시 시도해주세요'
    #     elif password != password_confirm:
    #         res_data['error'] = '비밀번호가 일치하지 않습니다. 다시 시도해주세요'
    #     else:
    #         cuser = CustomUser(username=username, email=email, password=make_password(password))
    #         cuser.save()
    #     return render(request, 'todoapp/signup.html', res_data)

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('your account has been avtivate')
    else:
        return HttpResponse('activation link is invalid')

# Login & Logout
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/login.html', {'form': AuthenticationForm()})
        else:
            login(request, user)
            return redirect('index')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')