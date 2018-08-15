from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Job
from alfa.forms import JobForm
from alfa.decorators import *

def jobs_page(request):
	context = {'all_jobs': Job.objects.all()}
	return render(request, 'jobs/jobs_page.html', context)

@has_premission()
def new_job_page(request):
	context = {'form': JobForm()}
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			job_object = Job()
			job_object.name = form.cleaned_data['name']
			job_object.description = form.cleaned_data['description']
			job_object.save()
			return HttpResponseRedirect(reverse('jobs_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
	return render(request, 'jobs/new_edit_job_page.html', context)

@has_premission()
def edit_job_page(request, id):
	context = {'form': JobForm()}
	try:
		job = Job.objects.get(id=id)
	except Job.DoesNotExist:
		return HttpResponseRedirect(reverse('jobs_url'))
	context['job'] = job
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			job.name = form.cleaned_data['name']
			job.description = form.cleaned_data['description']
			job.save()
			return HttpResponseRedirect(reverse('jobs_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
	return render(request, 'jobs/new_edit_job_page.html', context)

@has_premission()
def remove_job_page(request, id):
	context = {}
	try:
		job = Job.objects.get(id=id)
	except Job.DoesNotExist:
		return HttpResponseRedirect(reverse('jobs_url'))
	if request.method == 'POST':
		job.delete()
	else:
		context['text'] = 'Действительно удалить вакансию \"' + job.name + '\"' + '?'
		context['back_url'] = reverse('jobs_url')
		return render(request, 'admin/really_remove_page.html', context)
	return HttpResponseRedirect(reverse('jobs_url'))
