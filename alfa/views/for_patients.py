from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Document
from alfa.forms import DocumentForm

def for_patients_page(request):
	context = {}
	documents = Document.objects.filter(type='for_patients').all()
	context['documents'] = documents
	return render(request, 'for_patients/for_patients_page.html', context)

def new_for_patients_page(request):
	context = {}
	form = DocumentForm()
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			document = Document()
			document.name = form.cleaned_data['name']
			document.file = form.cleaned_data['file']
			document.type = 'for_patients'
			document.save()
			return HttpResponseRedirect(reverse('for_patients_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, 'for_patients/new_for_patients_page.html', context)
	else:
		context['form'] = form
		return render(request, 'for_patients/new_for_patients_page.html', context)
