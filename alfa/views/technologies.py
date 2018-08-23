from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Technology
from alfa.forms import NewTechnologyForm, EditTechnologyForm

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
def new_technology_page(request, id=None):
	#technology = get_object_or_404(Technology, id=id) if id else None
	context = {}
	context['form'] = NewTechnologyForm()
	if request.method == 'GET':
		return render(request, 'technologies/new_technology_page.html', context)
	if request.method == 'POST':
		form = TechForm(request.POST, request.FILES)
		if form.is_valid():
			technology = form.save()
			# technology.name = form.cleaned_data['name']
			# technology.img = form.cleaned_data['img']
			# technology.text = form.cleaned_data['text']
			# technology.save()
			return HttpResponseRedirect(reverse('edit_technology_url', args=(technology.id,)))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.\n' + str(form.errors)
			return render(request, 'technologies/new_technology_page.html', context)
	else:
		return HttpResponseRedirect(reverse('technologies_url'))

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
	template_name = 'technologies/new_technology_page.html'
	try:
		try:
			technology = Technology.objects.get(id=id)
		except Technology.DoesNotExist:
			return HttpResponseRedirect(reverse('technologies_url'))
		context['form'] = EditTechnologyForm(instance=technology)
		if request.method == 'GET':
			return render(request, template_name, context)
		if request.method == 'POST':
			form = EditTechnologyForm(request.POST, request.FILES, instance=technology)
			if form.is_valid():
				technology = form.save()
				return HttpResponseRedirect(reverse('edit_technology_url', kwargs={'id': technology.id}))
			else:
				context['error'] = True
				context['error_message'] = 'Неверно заполнена форма.\n' + str(form.errors)
				return render(request, template_name, context)
		return HttpResponseRedirect(reverse('technologies_url'))
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.\n' + str(e.message)
		return render(request, template_name, context)
