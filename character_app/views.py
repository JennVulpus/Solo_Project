import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Campaign, User, Character
import bcrypt

def create_campaign(request):
    if request.method == 'POST':
        errors = Campaign.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/create_campaign')
        else:
            Campaign.objects.create(
                name = request.POST['name'],
                owner = User.objects.get(id=request.session['userid']),
                session_date = request.POST['session_date'],
                desc = request.POST['desc'])
            return redirect('/dashboard')
    else:
        return redirect('/')

def create_character(request):
    if request.method == 'POST':
        errors = Character.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/create_character')
        else:
            Character.objects.create(
                name = request.POST['name'],
                specialty = request.POST['specialty'],
                race = request.POST['race'],
                background = request.POST['background'],
                strength = request.POST['strength'],
                dexterity = request.POST['dexterity'],
                constitution = request.POST['constitution'],
                intelligence = request.POST['intelligence'],
                wisdom = request.POST['wisdom'],
                charisma = request.POST['charisma'],
                desc = request.POST['desc'],
                owner = User.objects.get(id=request.session['userid']))
            return redirect('/dashboard')
    else:
        return redirect('/')


def dashboard(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid']),
            'owners' : Campaign.objects.filter(owner=User.objects.get(id=request.session['userid'])),
            'members' : Campaign.objects.filter(member=User.objects.get(id=request.session['userid'])),
            'others' : Campaign.objects.exclude(owner=User.objects.get(id=request.session['userid'])),
            'characters' : Character.objects.filter(owner=User.objects.get(id=request.session['userid']))
        }
        return render(request,'dashboard.html',context)

def delete_campaign(request,campaign_id):
    if 'userid' in request.session:
        campaign_to_delete = Campaign.objects.get(id=campaign_id)
        campaign_to_delete.delete()
        return redirect('/dashboard')
    else:
        return redirect ('/')

def delete_character(request,character_id):
    if 'userid' in request.session:
        character_to_delete = Character.objects.get(id=character_id)
        character_to_delete.delete()
        return redirect('/dashboard')
    else:
        return redirect('/')

def edit_campaign(request,campaign_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context ={
            'user' : User.objects.get(id=request.session['userid']),
            'campaign' : Campaign.objects.get(id=campaign_id)
        }
    return render(request,'edit_campaign.html',context)

def edit_character(request,character_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid']),
            'character' : Character.objects.get(id=character_id)
        }
    return render(request,'edit_character.html',context)

def index(request):
    return render(request, 'index.html')

def join(request, campaign_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        campaign = Campaign.objects.get(id = campaign_id)
        user = User.objects.get(id = request.session['userid'])
        campaign.member.add(user)
        campaign.save()
        return redirect('/dashboard')

def leave(request, campaign_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        campaign = Campaign.objects.get(id= campaign_id)
        user = User.objects.get(id =request.session['userid'])
        campaign.member.remove(user)
        campaign.save()
        return redirect('/dashboard')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        logged_user = User.objects.filter(email = request.POST['email'])
        request.session['userid'] = logged_user[0].id
        return redirect('/dashboard')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hash_pw)
            request.session['userid'] = User.objects.last().id
            return redirect('/dashboard')
    else:
        return redirect('/')

def render_create_campaign(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid'])
        }
        return render(request, 'create_cam.html',context)

def render_create_character(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid'])
        }
        return render(request,'create_character.html',context)

def save_campaign(request, campaign_id):
    if request.method == 'POST':
        errors = Campaign.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_campaign/{{campaign.id}}')
        else:
            update_campaign = Campaign.objects.get(id=campaign_id)
            update_campaign.name = request.POST['name']
            update_campaign.session_date = request.POST['session_date']
            update_campaign.desc = request.POST['desc']
            update_campaign.save()
            return redirect('/dashboard')
    else:
        return redirect('/')

def save_character(request,character_id):
    if request.method =='POST':
        errors = Character.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_character/{{character.id}}')
        else:
            update_character = Character.objects.get(id=character_id)
            update_character.name = request.POST['name']
            update_character.specialty = request.POST['specialty']
            update_character.race = request.POST['race']
            update_character.background = request.POST['background']
            update_character.strength = request.POST['strength']
            update_character.dexterity = request.POST['dexterity']
            update_character.constitution = request.POST['constitution']
            update_character.intelligence = request.POST['intelligence']
            update_character.wisdom = request.POST['wisdom']
            update_character.charisma = request.POST['charisma']
            update_character.desc = request.POST['desc']
            update_character.save()
            return redirect('/dashboard')
    else:
        return redirect('/')


def view_campaign(request,campaign_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context ={
            'user' : User.objects.get(id=request.session['userid']),
            'campaign' : Campaign.objects.get(id = campaign_id)
        }
        return render(request,'view_campaign.html',context)

def view_character(request,character_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id = request.session['userid']),
            'character' : Character.objects.get(id = character_id)
        }
        return render(request,'view_character.html',context)

