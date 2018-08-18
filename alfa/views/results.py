from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Doctor, Result
from alfa.forms import ResultForm

def results_page(request):
	context = {}
	context['doctors'] = Doctor.objects.all()
	return render(request, 'results/results_page.html', context)

@has_premission()
def new_result_page(request):
	context = {}
	template_name = 'results/new_result_page.html'
	if request.method == 'POST':
		form = ResultForm(request.POST, request.FILES)
		if form.is_valid():
			item = form.save()
			# item = Result()
			# print(form.cleaned_data['doctor'])
			# item.doctor.add(form.cleaned_data['doctor'])
			# item.img_after = form.cleaned_data['img_after']
			# item.img_before = form.cleaned_data['img_before']
			# item.text = form.cleaned_data['text']
			# item.save()
			return HttpResponseRedirect(reverse('results_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.\n' + str(form.errors)
			context['form'] = form
			return render(request, template_name, context)
	else:
		context['form'] = ResultForm()
		return render(request, template_name, context)

@has_premission()
def remove_result_page(request, id):
	context = {}
	try:
		result = Result.objects.get(id=id)
	except Result.DoesNotExist:
		return HttpResponseRedirect(reverse('results_url'))
	if request.method == 'POST':
		result.delete()
		return HttpResponseRedirect(reverse('results_url'))
	else:
		context['back_url'] = reverse('results_url')
		context['text'] = 'Действительно удалить \"' + result.text + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)

@has_premission()
def edit_result_page(request, id):
	context = {}
	return HttpResponse('ok')
