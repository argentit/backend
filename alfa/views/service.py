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
def new_service_page(request):
	context = {}
	context['form'] = ServiceForm()
	if request.method == 'POST':
		form = ServiceForm(request.POST)
		if form.is_valid():
			service_object = Service()
			service_object.name = form.cleaned_data['name']
			service_object.price = form.cleaned_data['price']
			service_object.description = form.cleaned_data['description']
			service_object.save()
			return HttpResponseRedirect(reverse('services_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'service/new_service_page.html', context)
	return render(request, 'service/new_service_page.html', context)

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
def edit_service_page(request, id):
	return HttpResponse('ok')
