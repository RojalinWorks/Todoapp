from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        password = request.POST.get('password1')
        print(fnm, emailid, password)
        my_user = User.objects.create_user(username=fnm, email=emailid, password=password)
        my_user.save()
        return redirect('/loginn')  # Assuming you have a login view to redirect to after signup
    
    return render(request, 'signup.html')
def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        password = request.POST.get('password1')
        print(fnm, password)
        user= authenticate(request, username=fnm, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todopage')
        else:
            return redirect('/loginn')
    return render(request, 'loginn.html')


@login_required(login_url='/loginn')  # Ensure user is logged in to access this view
def todo(request):
    if request.method == "POST":
        title=request.POST.get('title')

        obj = models.TODOO(title=title, user=request.user)
        obj.save()
        res=models.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, "todo.html", {'res': res})



@login_required(login_url='/loginn') 
def edit_todo(request,srno):
    if request.method == "POST":
        title=request.POST.get('title')

        obj = models.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        user= request.user
        res=models.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    obj = models.TODOO.objects.get(srno=srno)
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, "edit_todo.html", {'res': res})


@login_required(login_url='/loginn') 
def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return redirect('/todopage', {'res': res})

def signout(request):
    logout(request)
    return redirect('/loginn')  # Redirect to login page after signout