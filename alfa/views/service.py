from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Service, Doctor, SubService
from alfa.forms import ServiceForm, SubServiceForm

def services_page(request):
	context = {}
	context['services'] = Service.objects.all()
	return render(request, 'service/services_page.html', context)

def service_page(request, id):
	context = {}
	try:
		service = Service.objects.get(id=id)
	except Service.DoesNotExist:
		return render(request, 'service/services_page.html', context)
	service.sub_services = service.sub_service.all()
	if service.type == 'имплантация':
		for sub_service in service.sub_services:
			sub_service.prices = sub_service.price.split(';')
			if len(sub_service.prices) > 3 :
				sub_service.prices = sub_service.prices[:3]
			elif len(sub_service.prices) < 3:
				sub_service.prices.append(' ')
				if len(sub_service.prices) < 3:
					sub_service.prices.append(' ')
					if len(sub_service.prices) < 3:
						sub_service.prices.append(' ')
	context['service'] = service
	return render(request, 'service/service_page.html', context)

@has_premission()
def new_service_page(request, id=None):
	context = {}
	template_name = 'service/new_service_page.html'
	try:
		service = Service.objects.get(id=id)
		context['title'] = 'Изменить услугу'
	except Service.DoesNotExist:
		service = None
		context['title'] = 'Добавить услугу'
	try:
		if request.method == 'GET':
			context['form'] = ServiceForm(instance=service)
			return render(request, template_name, context)
		if request.method == 'POST':
			form = ServiceForm(request.POST, instance=service)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('services_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.\n' + str(form.error)
				return render(request, template_name, context)
		return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.\n' + e.message
		return render(request, template_name, context)

@has_premission()
def remove_service_page(request, id):
	context = {}
	try:
		service = Service.objects.get(id=id)
	except Service.DoesNotExist:
		return HttpResponseRedirect(reverse('services_url'))
	if request.method == 'POST':
		service.delete()
		return HttpResponseRedirect(reverse('services_url'))
	else:
		context['service'] = service
		context['back_url'] = reverse('services_url')
		context['text'] = 'Действительно удалить услугу \"' + service.name + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)

@has_premission()
def new_sub_service_page(request, s_id, id=None):
	context = {}
	template_name = 'service/edit_sub_service_page.html'
	try:
		s_obj = Service.objects.get(id=s_id)
		context['service'] = s_obj
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.\n' + e.message
		return render(request, template_name, context)
	try:
		service = SubService.objects.get(id=id)
		context['title'] = 'Изменить подуслугу к услуге \"' + s_obj.name +'\"'
	except SubService.DoesNotExist:
		service = None
		context['title'] = 'Добавить подуслугу к услуге \"' + s_obj.name +'\"'
	try:
		if request.method == 'GET':
			context['form'] = SubServiceForm(instance=service)
			return render(request, template_name, context)
		if request.method == 'POST':
			form = SubServiceForm(request.POST, instance=service)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.service = s_obj
				obj.save()
				return HttpResponseRedirect(reverse('service_url', kwargs={'id': s_id}))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.\n' + str(form.error)
				return render(request, template_name, context)
		return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.\n' + str(e)
		return render(request, template_name, context)

@has_premission()
def del_sub_service_page(request, s_id, id):
	context = {}
	back_url = reverse('service_url', kwargs={'id':s_id})
	try:
		sub_service = SubService.objects.get(id=id)
	except SubService.DoesNotExist:
		return HttpResponseRedirect(back_url)
	if request.method == 'POST':
		sub_service.delete()
		return HttpResponseRedirect(back_url)
	else:
		context['service'] = sub_service
		context['back_url'] = back_url
		context['text'] = 'Действительно удалить подуслугу \"' + sub_service.name + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)
