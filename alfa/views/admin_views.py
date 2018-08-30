from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from alfa.models import *
from alfa.forms import *
from django.conf import settings
from alfa.decorators import *
import datetime

context = {'all_servises': Service.objects.all()}

def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect(reverse('admin_auth_url'))

def admin_auth_page(request):
	context = {}
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
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'admin/admin_auth_page.html', context)

def new_home_item_page(request):
	return HttpResponseRedirect(reverse('home_url'))

def edit_text_page(request, id=None):
	context = {}
	template_name = 'admin/adit_text_page.html'
	try:
		try:
			if id is not None:
				text = Text.objects.get(id=None)
			else:
				text = None
		except Text.DoesNotExist:
			text = None
		form = TextModelForm(instance=text)
		if request.method == 'POST':
			return render(request, template_name, context)
		else:
			context['form'] = form
			return render(request, template_name, context)

	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = form
		return render(request, template_name, context)
