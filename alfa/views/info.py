from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Document
from alfa.forms import DocumentForm
from alfa.decorators import *

def info_page(request):
	print(reverse('remove_info_url', kwargs={'id':1}))
	context = {}
	documents = Document.objects.filter(type='info').all()
	context['documents'] = documents
	return render(request, 'info/info_page.html', context)

@has_premission()
def new_info_page(request):
	context = {}
	form = DocumentForm()
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			document = Document()
			document.name = form.cleaned_data['name']
			document.file = form.cleaned_data['file']
			document.type = 'info'
			document.save()
			return HttpResponseRedirect(reverse('info_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'info/new_info_page.html', context)
	else:
		context['form'] = form
		return render(request, 'info/new_info_page.html', context)

@has_premission()
def edit_info_page(request, id):
	return HttpResponseRedirect(reverse('info_url'))

@has_premission()
def remove_info_page(request, id):
	try:
		obj = Document.objects.get(id=id)
	except Document.DoesNotExist:
		return HttpResponseRedirect(reverse('info_url'))
	context = {}
	context['text'] = 'Действительно удалить документ \"' + obj.name + '\"' + '?'
	context['back_url'] = reverse('info_url')
	if request.method == 'POST':
		obj.delete()
		return HttpResponseRedirect(context['back_url'])
	return render(request, 'admin/really_remove_page.html', context)
