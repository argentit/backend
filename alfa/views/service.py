from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Service, Doctor
from alfa.forms import ServiceForm

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
