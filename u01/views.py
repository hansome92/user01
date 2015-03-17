from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import Http404
from django.contrib.auth.models import User
from forms import *
import views

# Create your views here.

def view(request):

    users = User.objects.all()
    res = []
    for u in users:
        #profile = u.get_profile()
        if u.is_superuser:
            continue
        profile = u.userprofile_set.all()
        birth = date.today()
        curdate = date.today()
        random = 0

        if profile.count() > 0:
            birth = profile[0].birthday
            random = profile[0].random
        else :
            profile = None


        bizzfuzz = ''
        if random > 0:
            biz = random % 3
            fuzz = random % 5
            if biz == 0:
                bizzfuzz = 'Bizz'
            if fuzz == 0:
                bizzfuzz += 'Fuzz'

        if bizzfuzz == '':
            bizzfuzz = str(random)

        year = curdate.year - birth.year

        perm = "blocked"
        if (year > 13) :
            perm = "allowed"


        res.append({'username' : u.username, 'birthday' : birth, 'eligible' : perm,
                    'random' : random, 'BizzFuzz' : bizzfuzz })

    return render_to_response('view.html', {'data' : res})

def edit(request, username):
    context = RequestContext(request)

    edit = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        u = User.objects.get(username=username)
        u.email = user_form.data['email']
        u.set_password(user_form.data['password'])


       # user = user_form.save(commit=False)
        #user.set_password(user.password)
        u.save()

        profile = UserProfile.objects.get(user=u)
        profile_form = UserProfileForm(data=request.POST)

        profile.birthday = profile_form.data['birthday']
        profile.random = profile_form.data['random']
        profile.save()

        return redirect(views.view)

    else:
        u = User.objects.get(username=username)
        profile = u.userprofile_set.all()
        if profile.count() > 0:
            profile = profile[0]
        else :
            profile = None
        u.password = ''
        user_form = UserForm(instance=u)
        profile_form = UserProfileForm(instance=profile)
        edit = True
    return render_to_response('edit.html',  {'username' : username, 'user_form': user_form, 'profile_form': profile_form, 'edit' : edit}, context)

def add(request):
    context = RequestContext(request)

    add = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            add = True
            return redirect(views.view)
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('add.html',  {'user_form': user_form, 'profile_form': profile_form, 'add' : add}, context)

def delete(request, username):

    if request.method != 'POST':

        u = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=u)
        if profile is not None:
            profile.delete()
        u.delete()
    return redirect(views.view)