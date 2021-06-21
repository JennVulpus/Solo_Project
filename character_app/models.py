from django.db import models
from sre_constants import error
import re
import bcrypt 
from datetime import datetime

class UserManager(models.Manager):
    def register_validation(self,form):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        used_email = User.objects.filter(email = form['email'])
        if len(form['first_name']) < 1:
            errors['first_name'] = 'Invalid First Name'
        if len(form['last_name']) < 1:
            errors['last_name'] = 'Invalid Last Name'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email'
        elif used_email:
            errors['used'] = 'Email already in use'
        if len(form['password']) < 6:
            errors['password'] = 'Password should be 6 characters long'
        elif form['password'] != form['confirmpw']:
            errors['confirmpw'] = 'Passwords do not match'
        return errors
    
    def login_validation(self,form):
        errors = {}
        email = User.objects.filter(email = form['email'])
        if not email or not bcrypt.checkpw(form['password'].encode(), email[0].password.encode()):
            errors['wrong'] = 'Email or Password is wrong'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class CharacterManager(models.Manager):
    def validation(self,form):
        errors = {}
        if len(form['name']) < 1:
            errors['name'] = 'Please add a name'
        return errors

class Character(models.Model):
    CLASS_OPTIONS = (
        ('Barbarian','Barbarian'),
        ('Cleric','Cleric'),
        ('Druid','Druid'),
        ('Fighter','Fighter'),
        ('Monk','Monk'),
        ('Paladin','Paladin'),
        ('Ranger','Ranger'),
        ('Rogue','Rogue'),
        ('Sorcerer','Sorecer'),
        ('Warlock','Warlock'),
        ('Wizard','Wizard')
    )
    RACE_OPTIONS = (
        ('Dragonborn','Dragonborn'),
        ('Dwarf','Dwarf'),
        ('Elf','Elf'),
        ('Half-Elf','Half-Elf'),
        ('Halfling','Halfling'),
        ('Half-Orc','Half-Orc'),
        ('Human','Human'),
        ('Tiefling','Tiefling')
    )
    BACKGROUND_OPTIONS = (
        ('Acolyte','Acolyte'),
        ('Charlatan','Charlatan'),
        ('Criminal','Criminal'),
        ('Entertainer','Entertainer'),
        ('Folk Hero','Folk Hero'),
        ('Guild Artisan','Guild Artisan'),
        ('Hermit','Hermit'),
        ('Outlander','Outlander'),
        ('Noble','Noble'),
        ('Sage','Sage'),
        ('Sailor','Sailor'),
        ('Soldier','Soldier'),
        ('Urchin','Urchin')
    )
    name = models.CharField(max_length=60)
    specialty = models.CharField(max_length=15, choices=CLASS_OPTIONS)
    race = models.CharField(max_length=15, choices = RACE_OPTIONS)
    background = models.CharField(max_length = 20, choices= BACKGROUND_OPTIONS)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    desc = models.TextField()
    owner = models.ForeignKey(User, related_name='owned_characters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CharacterManager()

class CampaignManager(models.Manager):
    def validation(self,form):
        errors = {}
        if len(form['name']) < 5:
            errors['name'] = 'Name must be at least 5 characters long'
        if datetime.strptime(form['session_date'], '%Y-%m-%d') < datetime.now():
            errors['session_date'] = 'The next session cannot start in the past'
        return errors

class Campaign(models.Model):
    name = models.CharField(max_length = 30)
    owner = models.ForeignKey(User, related_name='owned_campaigns', on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name='campaigns')
    session_date = models.DateTimeField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CampaignManager()