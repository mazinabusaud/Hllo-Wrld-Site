from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from core.forms import JoinForm, LoginForm
import datetime
from programs.models import Program

@login_required(login_url='/login/')
def home(request):
    programs_db_public = Program.objects.select_related().filter(is_public=True)
    program_count = programs_db_public.count()
    programs_public_list = list(programs_db_public)
    table_data = Program.objects.all().filter(is_public=True)
    context={
    "programs_db_public":programs_db_public,
    "program_count":program_count,
    "programs_public_list":programs_public_list,
    "table_data":table_data
    }
    return render(request, 'core/home.html', context)
def about(request):
    return render(request, 'core/about.html')

def login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    auth_login(request,user)
                    # Send the user back to original page requested, or home page
                    next = request.POST.get('next', 'home')
                    return HttpResponseRedirect(next)
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'core/login.html', {"login_form": LoginForm() } )
    else:
        return render(request, 'core/login.html', { "login_form": LoginForm() })

@login_required(login_url='/login/')
def logout(request):
    # Log out the user.
    auth_logout(request)
    # Return to homepage.
    return redirect("/")

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            print(join_form.errors)
            return render(request, 'core/join.html', { "join_form": join_form })
    else:
        return render(request, 'core/join.html', { "join_form": JoinForm() })
