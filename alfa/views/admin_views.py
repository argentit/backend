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
	try:
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('home_url'))
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
					return HttpResponseRedirect(reverse('home_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.'
				return render(request, 'admin/admin_auth_page.html', context)
	except Exception as a:
		context['error'] = True
		context['form'] = AuthForm()
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		return render(request, template_name, context)


def new_home_item_page(request):
	return HttpResponseRedirect(reverse('home_url'))

@has_premission()
def edit_text_page(request, where, id=None):
	context = {}
	context['form'] = TextModelForm()
	context['back_url'] = reverse(where + '_url')
	if id is None:
		context['action'] = reverse('new_text_url', kwargs={'where': where})
	else:
		context['action'] = reverse('edit_text_url', kwargs={'id': id, 'where': where})
	if where == 'dms':
		name = 'ДМС'
	elif where == 'about':
		name = 'О нас'
	elif where == 'partners':
		name = 'Партнёры'
	context['header'] = 'Добавить текст в раздел \'' + name + '\''
	template_name = 'admin/edit_text_page.html'
	try:
		try:
			if id is not None:
				text = Text.objects.get(id=id)
			else:
				text = None
		except Text.DoesNotExist:
			text = None
		if request.method == 'POST':
			form = TextModelForm(request.POST, instance=text)
			if form.is_valid():
				text = form.save(commit=False)
				text.name = where
				text.save()
				return HttpResponseRedirect(reverse(where + '_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				return render(request, template_name, context)
			return render(request, template_name, context)
		else:
			context['form'] = TextModelForm(instance=text)
			return render(request, template_name, context)

	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		return render(request, template_name, context)

@has_premission()
def edit_meta_page(request, id):
	try:
		obj = PageMetaData.objects.get(id=id)
	except PageMetaData.DoesNotExist:
		return HttpResponseRedirect(reverse('home_url'))
	try:
		if request.method == 'POST':
			form = MetaDataForm(request.POST, instance=obj)
			if form.is_valid():
				form.save()
			else:
				raise form.errors
		else:
			raise 'Неверный метод хапроса'
		return HttpResponseRedirect(obj.url)
	except Exception as e:
		context['meta_form_error'] = True
		context['meta_form_error_message'] = 'Произошла ошибка.<br>' + str(e)
		return render(request, template_name, context)
