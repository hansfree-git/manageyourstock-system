from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.forms import RegisterForm

# Create your views here.

def register(request, template_name='registration/register.html'):
	form=RegisterForm()
	if request.method=='POST':
		form=RegisterForm(request.POST or None)
		if form.is_valid():
			username=form.cleaned_data['username']
			user=form.save()
			
			messages.success(request,'Account successfully created')

			return redirect('loginPage')
	return render(request, template_name, locals())


def loginPage(request, template_name='registration/login.html'):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)
	
		if user is not None:
			login(request,user)
			return redirect('home-page')
		else:
			messages.warning(request,'Username or password not correct')
	return render(request, template_name, locals())


def logoutPage(request, template_name='registration/logout.html'):
	logout(request)
	return redirect('loginPage')
	return render(request, template_name, locals())