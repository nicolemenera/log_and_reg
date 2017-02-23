from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'logReg/index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    register_check = Users.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['pwd'], request.POST['cpwd'])
    if 'error' in register_check:
        error = register_check['error']
        for msg in error:
            messages.error(request, msg)
        return redirect('/')
    else:
        user = Users.objects.filter(email=request.POST['email'])
        request.session['userid'] = user[0].id

    return redirect('/process')

def login(request):
    if request.method == "GET":
        return redirect('/')
    login_check = Users.objects.login(request.POST['email'],request.POST['pwd'])
    if 'error' in login_check:
        error = login_check['error']
        for msg in error:
            messages.error(request, msg)
        return redirect('/')
    else:
        user = Users.objects.filter(email=request.POST['email'])
        request.session['userid'] = user[0].id
    return redirect('/process')

def process(request):
    if 'userid' not in request.session:
        messages.error(request, "please login cheater")
        return redirect('/')
    context = {'loguser': Users.objects.get(id=request.session['userid'])}
    return render(request, 'logReg/success.html', context)

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    del request.session['userid']
    return redirect('/')
def any(request):
    return redirect('/')