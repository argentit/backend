from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from alfa.models import *
from alfa.forms import *
from django.conf import settings
import datetime



context = {'all_servises': Service.objects.all()}



def results_page(request):
	context['doctors'] = Doctor.objects.all()
	return render(request, 'results_page.html', context)

def comments_page(request):
	return render(request, 'comments_page.html', context)

def news_page(request):
	context['all'] = Article.objects.all()
	return render(request, 'news_page.html', context)

def job_page(request):
	return render(request, 'job_page.html', context)

def charity_page(request):
	context['all'] = Charity.objects.all()
	return render(request, 'charity_page.html', context)

def for_patients_page(request):
	return render(request, 'for_patients_page.html', context)

def info_page(request):
	return render(request, 'info_page.html', context)

def services_page(request):
	new_s = Service()
	new_s.name = 'new name' + str(Service.objects.count() + 1)
	#new_s.save()
	context['services'] = Service.objects.all()
	return render(request,'services_page.html',context)

def service_page(request, slug):
	return render(request,'services_page.html',context)

def main_page(request):
	#return HttpResponse(settings.MEDIA_ROOT+'img/doctors/default.jpg')

	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			doctor = Doctor()
			doctor.img = form.cleaned_data['image']
		else:
			return render(request, 'home_page.html',)

		doctor.name = 'Ivanov'+str(Doctor.objects.all().count())
		doctor.surname = 'Ivan'
		doctor.patronymic = 'Petrovich'
		doctor.exp = '1999-01-01'
		doctor.slug = 'slug'
		doctor.save()
		type = Doctors_type(name='alfa')
		type.save()
		doctor.type.add(type)
		type = Doctors_type(name='beta')
		type.save()
		doctor.type.add(type)
		type = Doctors_type(name='gamma')
		type.save()
		doctor.type.add(type)
		doctor.save()
	return render(request, 'home_page.html', context)

def doctor_page(request, doctor_slug):
	doctor = Doctor.objects.filter(slug=doctor_slug)
	if doctor:
		exp = doctor.all()[0].exp
		now = datetime.datetime.now()
		years = now.year - exp.year
		context['doctor'] = doctor.all()[0]
		context['exp'] = 'Стаж: ' + str(years) + ' лет'
		return render(request, 'doctor_page.html',context)
	else:
		return HttpResponseRedirect(reverse('doctors_url'))

def doctors_page(request):
	context['doctors'] = Doctor.objects.all()
	return render(request, 'doctors_page.html',context)
