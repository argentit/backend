from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Charity
from alfa.forms import CharityForm
from alfa.decorators import *

@has_premission()
def remove_charity_page(request, id):
	context = {}
	context['text'] = 'Действительно удалить?'
	context['back_url'] = reverse('charity_url')
	if request.method == 'POST':
		try:
			obj = Charity.objects.get(id=id)
		except Charity.DoesNotExist:
			return HttpResponseRedirect(context['back_url'])
		obj.delete()
		return HttpResponseRedirect(context['back_url'])
	return render(request, 'admin/really_remove_page.html', context)

@has_premission()
def edit_charity_page(request, id):
	context = {}
	try:
		obj = Charity.objects.get(id=id)
	except Charity.DoesNotExist:
		return HttpResponseRedirect(reverse('charity_url'))
	context['form'] = CharityForm()
	context['text'] = obj.text
	context['image'] = request.META['HTTP_HOST'] + obj.img.url
	context['object_id'] = id
	return render(request, 'charity/edit_charity_page.html', context)

@has_premission()
def new_charity_page(request):
	context = {}
	context['form'] = CharityForm()
	context['object_id'] = '0'
	if request.method == 'GET':
		context['error'] = False
		return render(request, 'charity/new_charity_page.html', context)
	if request.method == 'POST':
		form = CharityForm(request.POST, request.FILES)
		if form.is_valid():
			charity_object = Charity()
			charity_object.text = form.cleaned_data['text']
			type(form.cleaned_data['text'])
			charity_object.img = form.cleaned_data['img']
			charity_object.save()
			context['error'] = False
			return HttpResponseRedirect(reverse('charity_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
	return render(request, 'charity/new_charity_page.html', context)

def charity_page(request):
	context = {}
	context['all'] = Charity.objects.all()
	return render(request, 'charity/charity_page.html', context)
