from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Document, DMS, Text
from alfa.forms import DocumentForm, DMSForm, TextModelForm
from alfa.decorators import *

def for_patients_page(request):
	context = {}
	documents = Document.objects.filter(type='for_patients').all()
	context['documents'] = documents
	return render(request, 'for_patients/for_patients_page.html', context)


@has_premission()
def new_for_patients_page(request):
	context = {}
	template_name = 'for_patients/new_for_patients_page.html'
	try:
		if request.method == 'POST':
			form = DocumentForm(request.POST, request.FILES)
			if form.is_valid():
				document = form.save(commit=False)
				document.type = 'for_patients'
				document.save()
				return HttpResponseRedirect(reverse('for_patients_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				context['form'] = form
				return render(request, 'template_name, context')
		else:
			context['form'] = DocumentForm()
			return render(request, template_name, context)
		return HttpResponseRedirect(reverse('for_patients_url'))
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = DocumentForm()
		return render(request, template_name, context)


@has_premission()
def edit_for_patients_page(request, id):
	context = {}
	template_name = 'for_patients/new_for_patients_page.html'
	try:
		document = Document.objects.get(id=id)
	except Document.DoesNotExist:
		return HttpResponseRedirect(reverse('for_patients_url'))
	try:
		if request.method == 'POST':
			form = DocumentForm(request.POST, request.FILES, instance=document)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('for_patients_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				context['form'] = form
				return render(request, template_name, context)
		else:
			context['form'] = DocumentForm(instance=document)
			return render(request, template_name, context)
		return HttpResponseRedirect(reverse('for_patients_url'))
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = DocumentForm(instance=document)
		return render(request, template_name, context)

@has_premission()
def remove_for_patients_page(request, id):
	try:
		obj = Document.objects.get(id=id)
	except Document.DoesNotExist:
		return HttpResponseRedirect(reverse('for_patients_url'))
	context = {}
	context['text'] = 'Действительно удалить документ \"' + obj.name + '\"' + '?'
	context['back_url'] = reverse('for_patients_url')
	if request.method == 'POST':
		obj.delete()
		return HttpResponseRedirect(context['back_url'])
	return render(request, 'admin/really_remove_page.html', context)

def dms_page(request):
	context = {}
	template_name = 'for_patients/dms_page.html'
	context['all_dms'] = DMS.objects.all()
	try:
		text = Text.objects.get(name='dms')
	except Text.DoesNotExist:
		text = None
	context['text'] = text
	return render(request, template_name, context)
	try:
		return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = str(e)
		return render(request, template_name, context)

@has_premission()
def new_dms_page(request, id=None):
	context = {}
	if id:
		context['title'] = 'Изменить ДМС'
	else:
		context['title'] = 'Добавить ДМС'
	template_name = 'for_patients/new_dms_page.html'
	try:
		if id:
			dms = DMS.objects.get(id=id)
		else:
			dms = None
	except DMS.DoesNotExist:
		dms = None
	try:
		if request.method == 'POST':
			form = DMSForm(request.POST, request.FILES, instance=dms)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('dms_url'))
			else:
				context['form'] = form
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				return render(request, template_name, context)
		else:
			context['form'] = DMSForm(instance=dms)
			return render(request, template_name, context)
	except Exception as e:
		context['form'] = DMSForm(instance=dms)
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		return render(request, template_name, context)

@has_premission()
def remove_dms_page(request, id):
	try:
		obj = DMS.objects.get(id=id)
	except DMS.DoesNotExist:
		return HttpResponseRedirect(reverse('dms_url'))
	context = {}
	context['text'] = 'Действительно удалить \"' + obj.name + '\"' + '?'
	context['back_url'] = reverse('dms_url')
	if request.method == 'POST':
		obj.delete()
		return HttpResponseRedirect(context['back_url'])
	return render(request, 'admin/really_remove_page.html', context)
