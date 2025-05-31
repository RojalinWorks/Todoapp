from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import TODOO
from django.contrib.auth import authenticate, login, logout

if signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        print(fnm, emailid, password)
        my_user = User.objects.create_user(username=fnm, email=emailid, password=password)
        my_user.save()
        return redirect('/loginn')  # Assuming you have a login view to redirect to after signup
    
    return render(request, 'signup.html')
def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        password = request.POST.get('password')
        print(fnm, password)
        user= authenticate(request, username=fnm, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todo')
        else:
            return render('/loginn')
    return render(request, 'loginn.html')