
from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import *
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import date

from .models import profiles
from .forms import * 

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tamilmatrimony:list')  # Replace 'home' with the name of your home URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated():
        messages.add_message(request,messages.SUCCESS,"You are already logged in!")
        return HttpResponseRedirect("/")
    username = password = ''
    context = RequestContext(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request,messages.SUCCESS,"Logged in successfully!")
                return HttpResponseRedirect('/')
            else: return HttpResponse("You're account is disabled.")
        else:
            messages.error(request,"username or Password invalid. Please try again!")
            return render(request, 'registration/login.html', {}, context)

    return render(request, 'registration/login.html', context_instance=context)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("/")


def profile_list(request):
    objectset = profiles.objects.all().order_by('-timestamp')[:10]
    print('ln 60 objectset ', objectset)
    for object in objectset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    context = {
        "objectset": objectset,
        "title": "list"
    }
    return render(request,"tamilmatrimony/index.html", context)
    #return HttpResponse("<h1>Hello World</h1>")


def profile_list_all(request):
    queryset = profiles.objects.all().order_by('-timestamp')
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    paginator = Paginator(queryset, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)
    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request,"tamilmatrimony/profiles.html", content)

def profile_search_list(request):
    queryset = profiles.objects.all().order_by('-timestamp')

    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query1 = request.GET.get('religion')
    query2 = request.GET.get('gender')
    query3 = request.GET.get('maritalstatus')
    query4 = request.GET.get('min_age')
    query5 = request.GET.get('max_age')

    if query1 :#and query2 and query3 and query4 and query5 :
        queryset = queryset.filter(religion__icontains=query1)#.filter( p_age_max__lte=query5)
        queryset = queryset.filter(age__gte=int(query4))
        queryset = queryset.filter(age__lte=int(query5))
        queryset = queryset.filter(gender=query2)
        queryset = queryset.filter(maritalStatus__icontains=query3)

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "page_list": queryset1,
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "tamilmatrimony/profile_search.html", content)
    #return HttpResponse("<h1>Hello World</h1>")

def profile_search_id(request):
    queryset = profiles.objects.all().order_by('-timestamp')
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query = request.GET.get('pid')
    if query:
        instance = get_object_or_404(profiles,pId=str(query))
        return HttpResponseRedirect(instance.get_absolute_url())

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "tamilmatrimony/profile_search_id.html", content)
    #return HttpResponse("<h1>Hello World</h1>")

@csrf_exempt
def profile_create(request):
    user_profile, created = profiles.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = Profileregister(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # return redirect('myprofile')
            return HttpResponseRedirect("/myprofile")
    else:
        form = Profileregister(instance=user_profile)
    return render(request, 'tamilmatrimony/create_profile.html', {'form': form, 'user_profile': user_profile})


@csrf_exempt
@login_required(login_url="/login/")
def myprofile_update(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        username = request.user.id
        print('ln 184 username ', username)
        instance = get_object_or_404(profiles, user=int(username))
        print('ln 186 instance ', instance)
        form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            print('ln 189 form.is_valid')            
            instance= form.save(commit=False)
            instance.save()
            print('ln 192 instance ', instance)
            messages.add_message(request,messages.SUCCESS,"Successfully updated your profile!")
            return HttpResponseRedirect("/myprofile")
        else:
            form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    else:
        messages.add_message(request,messages.ERROR,"Please login to edit your profile!")
        return HttpResponseRedirect("/login/")

    content = {
        "detail_object": instance,
        "title": "My Update Profile",
        "form":form,
    }
    return render(request, "tamilmatrimony/profileupdate.html", content)

'''
def profile_detail(request, slug=None):
    instance = get_object_or_404(profiles, slug=slug)

    def create_pid():
        if instance.pId == "TMG" :
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()

    content = {
        "detail_object": instance,
        "title": "Detail",

    }
    return render(request, "tamilmatrimony/view_profile.html", content)
'''

def profile_detail(request, slug):    
    instance = get_object_or_404(profiles, slug=slug)
    context = {
        "detail_object": instance,
    }
    return render(request, 'tamilmatrimony/view_profile.html', context)

@login_required(login_url='/login/')
def my_profile(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        username = request.user.id
        print('ln 235 username ', username)
        instance1 = profiles.objects.filter(user = int(username))#get_object_or_404(profiles, user = int(username))
        if not instance1:
            messages.add_message(request,messages.ERROR,"Please create an Profile!")
            return HttpResponseRedirect("/create")
        instance = get_object_or_404(profiles, user = int(username))
        print('ln 241 instance ', instance)

    else:
        messages.error(request, "Please login to view your profile!")
        return render(request, 'registration/login.html', {}, context)

    def create_pid():
        if instance.pId == "TMG" :
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()

    context = {
        "detail_object": instance,
        "title": "my_Detail",
    }
    return render(request, "tamilmatrimony/view_profile.html", context)


def profile_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    print('ln 294 instance.slug ', instance.slug)
    instance.delete()
    messages.success(request, "succesfully Deleted!")
    return redirect("profiles:list")


'''
@login_required(login_url="/login/")
def profile_create(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        userid = int(request.user.id)
        queryset = profiles.objects.filter(user=userid)
        if queryset:
            messages.error(request, "You have already created a profile!")
            # return HttpResponseRedirect('myprofile')
            # return redirect('myprofile')
            return redirect('tamilmatrimony:myprofile')

        form = Profileregister(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            if instance.pId == "TMG":
                instance.pId = "TMG" + "00" + str(instance.tmId)
                instance.save()
            messages.add_message(request,messages.SUCCESS,"Successfully created a profile!")
            return HttpResponseRedirect("/myprofile")
        else:
            form = Profileregister(request.POST or None, request.FILES or None)
    context = {
        "form": form,
        "title": "Create/Register"
    }

    # return render(request, "registration/register.html", context)
    return render(request, "tamilmatrimony/create_profile.html", context)
'''


@csrf_exempt
def profile_update(request, slug=None):
    print('ln 328 in views.profile_update')
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    print('ln 332 instance ', instance)
    form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        print('ln 337 instance ', instance)
        messages.success(request, "successfully updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Not updated!")
        print('ln 341 form.is_invalid')
    context = {
        "detail_object": instance,
        "title": "Update Profile",
        "form":form,
    }
    return render(request, "tamilmatrimony/profileupdate.html", context)


