from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_RE = re.compile(r'[a-zA-Z]\D{2,}$')

class UserManager(models.Manager):
    #order first_name, last_name, email, pwd, cpwd
    def register(self, *args):
        errormsg = []
        status = True
        if not NAME_RE.match(args[0]):
            errormsg.append('First name must be at least two letters in length, and contain no numbers')
            status = False
        if not NAME_RE.match(args[1]):
            errormsg.append('Last name must be at least two letters in length, and contain no numbers')
            status = False
        if len(Users.objects.filter(email=args[2])) > 0:
            errormsg.append('Email is already registered')
            status = False
        if not EMAIL_REGEX.match(args[2]):
            errormsg.append('Email invalid')
            status = False
        if len(args[3]) < 8:
            errormsg.append('Password must be longer than eight characters')
            status = False
        if args[3] != args[4]:
            errormsg.append('Passwords do not match')
            status = False
        if status == False:
            return {'error': errormsg}
        if status == True:
            password = args[3].encode()
            pwhash= bcrypt.hashpw(password,bcrypt.gensalt())
            super(UserManager, self).create(first_name=args[0], last_name=args[1], email=args[2], password=pwhash)
        return {'first_name': args[0], 'last_name': args[1], 'email' : args[2], 'password': args[3]}

    def login(self, email, password):
        errormsg = []
        status = True
        existing = Users.objects.filter(email=email)
        if len(existing) <= 0:
            errormsg.append('please provided registered credentials')
            status = False
        elif not existing:
            errormsg.append('not {} in database!'.format(request.POST['email']))
            status = False
        elif not bcrypt.checkpw(password.encode(), existing[0].password.encode()):
            errormsg.append('password does not match')
            status = False
        if status == False:
            return {'error': errormsg}
        else:
            return{ 'True': existing[0].id }


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()