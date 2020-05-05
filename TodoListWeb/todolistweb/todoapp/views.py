from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserSignUpForm, ResendEmailForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import TodoForm
from .models import Todo
import datetime

def get7Date():
    day = datetime.datetime.now().weekday()
    # 현재 년월일시분초
    current_datetime = datetime.datetime.now()
    dayofweek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    week = {}
    for i in range(0, 7):
        week[dayofweek[i]] = (current_datetime + datetime.timedelta(days=-day + i)).day
    return week

def get7dayMonth():
    day = datetime.datetime.now().weekday()
    # 현재 년월일시분초
    current_datetime = datetime.datetime.now()
    dayofweek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    month = {}
    for i in range(0, 7):
        month[dayofweek[i]] = (current_datetime + datetime.timedelta(days=-day + i)).strftime("%B")
    return month

def month_converter(month):
    months = ['January', 'February', 'March', 'April', 'May', 'Jun', 'July', 'August', 'September', 'October', 'November', 'December']
    return months.index(month) + 1

def get_all_week_todo(request):
    week = get7Date()
    month = get7dayMonth()
    all_week_todo = []

    mon_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['mon'], schedule_date__month=month_converter(month['mon']))
    tue_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['tue'], schedule_date__month=month_converter(month['tue']))
    wed_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['wed'], schedule_date__month=month_converter(month['wed']))
    thu_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['thu'], schedule_date__month=month_converter(month['thu']))
    fri_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['fri'], schedule_date__month=month_converter(month['fri']))
    sat_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['sat'], schedule_date__month=month_converter(month['sat']))
    sun_todo = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['sun'], schedule_date__month=month_converter(month['sun']))

    all_week_todo.append(mon_todo)
    all_week_todo.append(tue_todo)
    all_week_todo.append(wed_todo)
    all_week_todo.append(thu_todo)
    all_week_todo.append(fri_todo)
    all_week_todo.append(sat_todo)
    all_week_todo.append(sun_todo)
    return all_week_todo

# Create your views here.
def index(request):
    return render(request, 'todoapp/index.html')

@login_required()
def bootindex(request):
    week = get7Date()
    month = get7dayMonth()
    # todo_list = Todo.objects.filter(user=request.user, date_completed__isnull=True, schedule_date__day=week['mon'], schedule_date__month=month_converter(month['mon']))
    todo_list = get_all_week_todo(request)
    return render(request, 'bootstrapTemplate/ui-cards.html',
                  {
                    'week':week,
                    'month':month,
                    'todo_list':todo_list
                  }
                  )

##### Signup #####
def signupuser(request):
    if request.method == 'GET':
        form = UserSignUpForm()
    else:
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email and User.objects.filter(email=email).count() > 0:
                return render(request, 'registration/page-register.html', {'form': form, 'email_error':'That email is already exists. Please sign up with another email.'})
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                message = render_to_string('registration/activate_account.html',
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
                return render(request, 'registration/page-register-complete.html', {'complete_msg':'y'})
    return render(request, 'registration/page-register.html', {'form':form})

def resend_mail(request):
    if request.method == 'GET':
        form = ResendEmailForm()
    else:
        form = ResendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
               user = User.objects.get(email=email)
               if user.is_active:
                   return redirect('loginuser')
               else:
                   current_site = get_current_site(request)
                   email_subject = 'Activate your account'
                   message = render_to_string('registration/activate_account.html',
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
                   return render(request, 'registration/page-register-complete.html', {'complete_msg':'yes'})
            except User.DoesNotExist:
                return render(request, 'registration/resend_mail.html', {'form': form, 'error': 'y'})

    return render(request, 'registration/resend_mail.html', {'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        if user.is_active:
            return render(request, 'registration/page-register-complete.html', {'auth_already_done_msg':'Your email authentication was already done.'})
        elif account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'registration/page-register-complete.html', {'auth_complete_msg':'Your email authentication is Completed!'})
            # return render(request, 'todoapp/login.html', {'form': form, 'auth_complete_msg':'Email Authentication Complete!'})
    else:
        return render(request, 'registration/page-register-complete.html', {'invalid_link_msg':'Sorry, Your email link is invalid. Please sign up again.'})


##### Login & Logout #####
def loginuser(request):
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = 'form-control'
    form.fields['username'].widget.attrs['placeholder'] = 'Username'
    form.fields['password'].widget.attrs['class'] = 'form-control'
    form.fields['password'].widget.attrs['placeholder'] = 'Password'
    if request.method == 'GET':
        return render(request, 'registration/page-login.html', {'form':form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/page-login.html', {'form': form, 'error':'The account does not exist or the password does not match. <br>please check your account again.'})
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


##### mypage #####
def mypage(request):
    return render(request, 'todoapp/mypage.html')

def lock_screen(request):
    if request.method == 'GET':
        return render(request, 'bootstrapTemplate/page-lock.html')
    else:
        user = request.user
        input_password = request.POST.get('password')
        if user.check_password(input_password):
            return redirect('index')
        else:
            return render(request, 'bootstrapTemplate/page-lock.html', {'error':'Password does not match.'})


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


#################

@login_required
def create_todo(request, day):
    week = get7Date()
    month = get7dayMonth()
    now = datetime.datetime.now()
    form = TodoForm(request.POST)
    new_todo = form.save(commit=False)
    new_todo.schedule_date = datetime.datetime(now.year, month_converter(month[day]), week[day])
    new_todo.user = request.user
    new_todo.save()
    return redirect('index')

def todo_create(request, day):
    week = get7Date()
    month = get7dayMonth()
    now = datetime.datetime.now()

    if day == 'mon':
        render_list_url = 'todo/monday_todo_list.html'
    elif day == 'tue':
        render_list_url = 'todo/tuesday_todo_list.html'
    elif day == 'wed':
        render_list_url = 'todo/wednesday_todo_list.html'
    elif day == 'thu':
        render_list_url = 'todo/thursday_todo_list.html'
    elif day == 'fri':
        render_list_url = 'todo/friday_todo_list.html'
    elif day == 'sat':
        render_list_url = 'todo/saturday_todo_list.html'
    elif day == 'sun':
        render_list_url = 'todo/sunday_todo_list.html'

    data = dict()

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.schedule_date = datetime.datetime(now.year, month_converter(month[day]), week[day])
            new_todo.user = request.user
            new_todo.save()
            data['form_is_valid'] = True
            todo_list = get_all_week_todo(request)
            data['html_todo_list'] = render_to_string(render_list_url, {
                'todo_list': todo_list
            })
        else:
            data['form_is_valid'] = False
    else:
        form = TodoForm()

    context = {'form': form, 'day':day}
    data['html_form'] = render_to_string('todo/partial_todo_create.html',
                                         context,
                                         request=request,

                                         )
    return JsonResponse(data)

@login_required
def completed_todo(request):
    todo_list = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedTodo.html',{'todo_list':todo_list})

@login_required
def todo_detail(request, todo_pk):
    week = get7Date()
    month = get7dayMonth()
    todo_list = get_all_week_todo(request)
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'bootstrapTemplate/ui-cards.html', {
            'todo':todo,
            'form':form,
            'day': todo.schedule_date.day,
            'week': week,
            'month': month,
            'todo_list': todo_list,
        })
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('index')
        except ValueError:
            return redirect('index')

@login_required
def todo_delete(request, todo_pk, day):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    data = dict()

    if day == 'mon':
        render_list_url = 'todo/monday_todo_list.html'
    elif day == 'tue':
        render_list_url = 'todo/tuesday_todo_list.html'
    elif day == 'wed':
        render_list_url = 'todo/wednesday_todo_list.html'
    elif day == 'thu':
        render_list_url = 'todo/thursday_todo_list.html'
    elif day == 'fri':
        render_list_url = 'todo/friday_todo_list.html'
    elif day == 'sat':
        render_list_url = 'todo/saturday_todo_list.html'
    elif day == 'sun':
        render_list_url = 'todo/sunday_todo_list.html'

    if request.method == 'POST':
        todo.delete()
        data['form_is_valid'] = True
        todo_list = get_all_week_todo(request)
        data['html_todo_list'] = render_to_string(render_list_url, {'todo_list' : todo_list})
    else:
        context = {'todo' : todo, 'day' : day}
        data['html_form'] = render_to_string('todo/partial_todo_delete.html', context, request=request)

    return JsonResponse(data)

@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todo')

@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todo')