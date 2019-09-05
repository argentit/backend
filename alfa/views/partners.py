from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Document, DMS, Text, Partner
from alfa.forms import DocumentForm, DMSForm, TextModelForm, PartnerForm
from alfa.decorators import *

def partners_page(request):
	context = {}
	partners = Partner.objects.all()
	context['partners'] = partners
	try:
		text = Text.objects.get(name='partners')
	except Text.DoesNotExist:
		text = None
	context['text'] = text
	return render(request, 'partners/partners_page.html', context)


@has_premission()
def new_partner_page(request):
	context = {}
	template_name = 'partners/new_partner_page.html'
	try:
		if request.method == 'POST':
			form = PartnerForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('partners_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				context['form'] = form
				return render(request, template_name, context)
		else:
			context['form'] = PartnerForm()
			return render(request, template_name, context)
		return HttpResponseRedirect(reverse('for_patients_url'))
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = PartnerForm()
		return render(request, template_name, context)


@has_premission()
def edit_partner_page(request, id):
	context = {}
	template_name = 'partners/new_partner_page.html'
	try:
		document = Partner.objects.get(id=id)
	except Partner.DoesNotExist:
		return HttpResponseRedirect(reverse('partners_url'))
	try:
		if request.method == 'POST':
			form = PartnerForm(request.POST, request.FILES, instance=document)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('partners_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
				context['form'] = form
				return render(request, template_name, context)
		else:
			context['form'] = PartnerForm(instance=document)
			return render(request, template_name, context)
		return HttpResponseRedirect(reverse('partners_url'))
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = DocumentForm(instance=document)
		return render(request, template_name, context)

@has_premission()
def remove_partner_page(request, id):
	try:
		obj = Partner.objects.get(id=id)
	except Partner.DoesNotExist:
		return HttpResponseRedirect(reverse('partners_url'))
	context = {}
	context['text'] = 'Действительно удалить партнёра \"' + obj.name + '\"' + '?'
	context['back_url'] = reverse('partners_url')
	if request.method == 'POST':
		obj.delete()
		return HttpResponseRedirect(context['back_url'])
	return render(request, 'admin/really_remove_page.html', context)
