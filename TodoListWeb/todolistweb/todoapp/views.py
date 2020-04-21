from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserSignUpForm, ResendEmailForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import TodoForm

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
            email = form.cleaned_data.get('email')
            if email and User.objects.filter(email=email).count() > 0:
                return render(request, 'todoapp/signup.html', {'form': form, 'email_error':'y'})
            else:
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
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                return render(request, 'todoapp/signup.html')
    return render(request, 'todoapp/signup.html', {'form':form})

def resend_mail(request):
    if request.method == 'GET':
        form = ResendEmailForm()
    else:
        form = ResendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
               user = User.objects.get(email=email)
               print(user.pk)
               if user.is_active:
                   return redirect('loginuser')
               else:
                   current_site = get_current_site(request)
                   email_subject = 'Activate your account'
                   message = render_to_string('todoapp/activate_account.html',
                                              {
                                                  'user': user,
                                                  'domain': current_site.domain,
                                                  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                  'token': account_activation_token.make_token(user),
                                              }
                                              )
                   to_email = form.cleaned_data.get('email')
                   email = EmailMessage(email_subject, message, to=[to_email])
                   email.send()
                   return render(request, 'todoapp/signup.html')
            except User.DoesNotExist:
                return render(request, 'todoapp/resend_mail.html', {'form': form, 'msg': 'yes'})

    return render(request, 'todoapp/resend_mail.html', {'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = 'form-control'
    form.fields['password'].widget.attrs['class'] = 'form-control'

    if user is not None:
        if user.is_active:
            return render(request, 'todoapp/index.html', {'auth_already_done_msg':'Your email authentication is already completed. Please Login.'})
        elif account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'todoapp/index.html', {'auth_complete_msg':'Email Authentication Complete! Please Login.'})
            # return render(request, 'todoapp/login.html', {'form': form, 'auth_complete_msg':'Email Authentication Complete!'})
    else:
        return render(request, 'todoapp/signup.html', {'form': form, 'invalid_link_msg':'Sorry, Your activation link is invalid. Please sign up again.'})

# mypage
def mypage(request):
    return render(request, 'todoapp/mypage.html')

def password_change(request):
    if request.method == 'GET':
        return render(request, 'todoapp/password_change_form.html')
    else:
        current_password = request.POST.get('origin_password')
        user = request.user
        error = ''
        if check_password(current_password, user.password):
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return render(request, 'todoapp/index.html')
            else:
                error = 'new password & confirm password did not match'
        else:
            error = 'current password did not match'
        return render(request, 'todoapp/password_change_form.html', {'error':error})

# Login & Logout
def loginuser(request):
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = 'form-control'
    form.fields['password'].widget.attrs['class'] = 'form-control'
    if request.method == 'GET':
        return render(request, 'todoapp/login.html', {'form':form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/login.html', {'form': form, 'error':'The account does not exist or the password does not match. please check your account again.'})
        else:
            login(request, user)
            return redirect('index')

@login_required
def logoutuser(request):
    # if request.method == 'POST':
    #     logout(request)
    #     return redirect('index')
    logout(request)
    return redirect('index')


#################

# TodoApp
@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html')
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('index')
        except ValueError:
            return render(request, 'todo/createTodo.html', {'form': TodoForm(), 'error':'Value Error. Try again.'})