from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from alfa.models import *
from alfa.forms import *
from django.conf import settings
import datetime

context = {'all_servises': Service.objects.all()}

def has_premission():
	def has(f):
		def func(request, *args, **kwargs):
			if request.user.is_superuser:
				return f(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse('main_url'))
		return func
	return has



def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect(reverse('admin/admin_auth_url'))

def admin_auth_page(request):
	if request.method != 'POST':
		return render(request, 'admin/admin_auth_page.html', context)
	else:
		form = AuthForm(request.POST)
		if form.is_valid():
			user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
			if user is None:
				context['error'] = True
				context['error_message'] = 'Неверный логин и/или пароль.'
				print(context['error_message'])
				return render(request, 'admin/admin_auth_page.html', context)
			else:
				login(request, user)
				context['success'] = True
				context['success_message'] = 'Авторизация прошла успешно.'
				return render(request, 'admin/admin_auth_page.html', context)
		else:
			print(form.errors)
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'admin/admin_auth_page.html', context)

def new_doctor_page(request):
	context['form'] = NewDoctorForm()
	return render(request, 'admin/new_doctor_page.html', context)

def new_technology_page(request):
	return HttpResponse('ok')

def new_service_page(request):
	return HttpResponse('ok')

def new_result_page(request):
	if request.method == 'POST':
		form = NewResult(request.POST, request.FILES)
		if form.is_valid():
			#item = form.save(commit=False)
			item = Result()
			print(form.cleaned_data['img_after'])

			item.doctor = form.cleaned_data['doctor']
			item.img_after = form.cleaned_data['img_after']
			item.img_before = form.cleaned_data['img_before']
			item.text = form.cleaned_data['text']
			item.save()
			return HttpResponseRedirect(reverse('results_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			context['form'] = form
			return render(request, 'admin/new_result_page.html', context)
	context['form'] = NewResult()
	return render(request, 'admin/new_result_page.html', context)

def remove_result_page(request, id):
	try:
		item = Result.objects.get(id=id)
	except Result.DoesNotExist:
		return HttpResponseRedirect(reverse('results_url'))
	item.delete()
	return HttpResponseRedirect(reverse('results_url'))



@has_premission()
def new_home_item_page(request):
	return HttpResponse('ok')

def remove_charity_page(request, id):
	return HttpResponse('ok')

def edit_charity_page(request, id):
	return HttpResponse('ok')

def new_charity_page(request):
	context['form'] = CharityForm()
	if request.method == 'POST':
		form = CharityForm(request.POST, request.FILES)
		if form.is_valid():
			charity_object = Charity()
			charity_object.text = form.cleaned_data['text']
			charity_object.img = form.cleaned_data['img']
			charity_object.save()
			return HttpResponseRedirect(reverse('charity_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
	return render(request, 'admin/new_charity_page.html', context)
	#else:
	#	return render(request, 'admin/new_charity_page.html', context)
