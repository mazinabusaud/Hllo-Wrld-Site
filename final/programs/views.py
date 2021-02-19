from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from programs.models import Program, ProgramCategory
from programs.forms import NewProgramForm, EditProgramForm, OnlyPublicProgramsForm
from core.models import UserProfile
from django.contrib.auth.models import User
import os

from rest_framework import viewsets
from rest_framework import permissions
from programs.serializers import ProgramSerializer, ProgramCategorySerializer, UserSerializer

# Create your views here.
@login_required(login_url='/login/')
def programs(request):
    # Create some default categories if there aren't any.
    if (not ProgramCategory.objects.all()):
        ProgramCategory.objects.create(category="Hobby")
        ProgramCategory.objects.create(category="School")
        ProgramCategory.objects.create(category="Work")

    if (request.method == "GET" and "toggle_public" in request.GET):
        id = request.GET["toggle_public"]
        program = Program.objects.get(id=id)
        program.is_public = not program.is_public
        program.save()
    
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Program.objects.all().filter(id=id).delete()
        return redirect("/programs/")

    if (request.method == "POST"):
        try:
            user_profile = UserProfile.objects.filter(user=request.user).get()
        except:
            user_profile = UserProfile()
            user_profile.user = request.user
            user_profile.show_public_programs = False
        
        form = OnlyPublicProgramsForm(request.POST, instance=user_profile)

        if (form.is_valid()):
            form.save()
    try:
        user_profile = UserProfile.objects.filter(user=request.user).get()
        show_public_data = OnlyPublicProgramsForm(instance=user_profile)
    except:
        show_public_data = OnlyPublicProgramsForm()

    show_public = show_public_data["show_public_programs"].value()
    
    if(show_public):
        table_data = Program.objects.select_related().filter(user=request.user, is_public=False)
    else:
        table_data = Program.objects.all().filter(user=request.user)
    #filename = Program.objects.all().filter(user=request.user).values_list('upload')
    context = {
        "show_public_data":show_public_data,
        "table_data": table_data,
    }
    return render(request, 'programs/programs.html', context)

def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            new_program_form = NewProgramForm(request.POST, request.FILES)
            if (new_program_form.is_valid()):
                description = new_program_form.cleaned_data["description"]
                category = new_program_form.cleaned_data["category"]
                user = User.objects.get(id=request.user.id)
                newupload = Program(user = user, description=description, category=category, is_public=False, upload=request.FILES['upload']).save()
                return redirect("/programs/")
            else:
                context = {
                    "form_data": new_program_form
                }
                return render(request, 'programs/add.html', context)
        else:
            # Cancel
            return redirect("/programs/")

    else:
        context = {
            "form_data": NewProgramForm()
        }
        return render(request, 'programs/add.html', context)

def edit(request, id):
    if (request.method == "GET"):
        program = Program.objects.get(id=id)
        form = EditProgramForm(instance=program)
        context = { "form_data" : form }
        return render(request, 'programs/edit.html', context)

    if (request.method == "POST"):
        if ("update" in request.POST):
            form = EditProgramForm(request.POST, request.FILES)
            if (form.is_valid()):
                program = form.save(commit=False)
                program.user = request.user
                program.id = id
                program.save()
                return redirect("/programs/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'programs/add.html', context)
        else:
            #Cancel
            return redirect("/programs/")

class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Programs to be viewed or edited.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Program Categories to be viewed or edited.
    """
    queryset = ProgramCategory.objects.all()
    serializer_class = ProgramCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
