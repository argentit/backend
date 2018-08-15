from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Technology
from alfa.forms import TechnologyForm

def technologies_page(request):
	context = {}
	context['technologies'] = Technology.objects.all()
	return render(request, 'technologies/technologies_page.html', context)

def technology_page(request, id):
	context = {}
	try:
		technology = Technology.objects.get(id=id)
	except Technology.DoesNotExist:
		context['technologies'] = Technology.objects.all()
		return render(request, 'technologies/technologies_page.html', context)
	context['technology'] = technology
	return render(request, 'technologies/technology_page.html', context)

@has_premission()
def new_technology_page(request):
	context = {}
	context['form'] = TechnologyForm()
	if request.method == 'GET':
		return render(request, 'technologies/new_technology_page.html', context)
	if request.method == 'POST':
		form = TechnologyForm(request.POST, request.FILES)
		if form.is_valid():
			charity_object = Technology()
			charity_object.name = form.cleaned_data['name']
			charity_object.img = form.cleaned_data['file']
			charity_object.text = form.cleaned_data['description']
			charity_object.save()
			return HttpResponseRedirect(reverse('technologies_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'technologies/new_technology_page.html', context)

@has_premission()
def remove_technology_page(request, id):
	context = {}
	try:
		technology = Technology.objects.get(id=id)
	except Technology.DoesNotExist:
		return HttpResponseRedirect(reverse('technologies_url'))
	if request.method == 'POST':
		technology.delete()
		return HttpResponseRedirect(reverse('technologies_url'))
	else:
		context['technology'] = technology
		context['back_url'] = reverse('technologies_url')
		context['text'] = 'Действительно удалить технологию \"' + technology.name + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)

@has_premission()
def edit_technology_page(request, id):
	context = {}
	return HttpResponse('ok')
