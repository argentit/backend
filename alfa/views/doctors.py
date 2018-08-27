from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import  Doctor, Practice, Education, Certificate, Doctors_type, Service, Technology
from alfa.forms import DoctorForm, TextForm, ImageForm, SelectServiceForm, SelectTechnologyForm
from datetime import date

def doctors_page(request):
	context = {}
	context['doctors'] = Doctor.objects.all()
	return render(request, 'doctors/doctors_page.html', context)

def doctor_page(request, id):
	context = {}
	template_name = 'doctors/doctor_page.html'
	try:
		doctor = Doctor.objects.get(id=id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	context['doctor'] = doctor
	def num_years(begin, end=None):
		from datetime import datetime
		def yearsago(years, from_date=None):
			if from_date is None:
				from_date = datetime.now()
			try:
				return from_date.replace(year=from_date.year - years)
			except ValueError:
				assert from_date.month == 2 and from_date.day == 29
				return from_date.replace(month=2, day=28, year=from_date.year-years)
		if end is None:
			end = date.today()
		num_years = int((end - begin).days / 365.25)
		if begin > yearsago(num_years, end):
			return num_years - 1
		else:
			return num_years
	years = num_years(doctor.exp)
	if years % 10 == 1:
		context['years'] = str(years) + ' год'
	elif years % 10 == 2 or years % 10 == 3 or years % 10 == 4:
		context['years'] = str(years) + ' года'
	else:
		context['years'] = str(years) + ' лет'
	
	return render(request, template_name, context)

@has_premission()
def new_doctor_page(request):
	context = {}
	template_name = 'doctors/new_doctor_page.html'
	if request.method == 'POST':
		form = DoctorForm(request.POST, request.FILES)
		if form.is_valid():
			doctor = Doctor()
			doctor.number = str(doctor.id)
			doctor.name = form.cleaned_data['name']
			doctor.surname = form.cleaned_data['surname']
			doctor.patronymic = form.cleaned_data['patronymic']
			doctor.exp = form.cleaned_data['exp']
			doctor.photo = form.cleaned_data['photo']
			doctor.save()
			doctor.number = str(doctor.id)
			doctor.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = DoctorForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	context['form'] = DoctorForm()
	return render(request, template_name, context)

@has_premission()
def  edit_doctor_page(request, id):
	return HttpResponse('ok')

@has_premission()
def remove_doctor_page(request, id):
	context = {}
	try:
		doctor = Doctor.objects.get(id=id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		doctor.delete()
		return HttpResponseRedirect(reverse('doctors_url'))
	else:
		context['doctor'] = doctor
		context['back_url'] = reverse('doctors_url')
		context['text'] = 'Действительно удалить доктора \"' + str(doctor) + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)




@has_premission()
def new_practice_page(request, doctor_id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Добавить напривление'
	context['label'] = 'Направление'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			practice = Practice()
			#practice.doctor = doctor
			practice.name = form.cleaned_data['name']
			practice.save()
			doctor.practice.add(practice)
			doctor.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		return render(request, template_name, context)

@has_premission()
def new_education_page(request, doctor_id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Добавить образование'
	context['label'] = 'Образование'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			education = Education()
			education.doctor = doctor
			education.name = form.cleaned_data['name']
			education.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		return render(request, template_name, context)

@has_premission()
def edit_education_page(request, doctor_id, id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Изменить образование'
	context['label'] = 'Образование'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		education = Education.objects.get(id=id)
	except Education.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			education.name = form.cleaned_data['name']
			education.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			context['default_value'] = request.POST['name']
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		context['default_value'] = education.name
		return render(request, template_name, context)

@has_premission()
def edit_practice_page(request, doctor_id, id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Изменить напривление'
	context['label'] = 'Направление'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		practice = Practice.objects.get(id=id)
	except Practice.DoesNotExist:
		return HttpResponseRedirect(reverse('doctorr_url', kwargs={'id': doctor.id}))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			practice.name = form.cleaned_data['name']
			practice.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			context['default_value'] = request.POST['name']
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		context['default_value'] = practice.name
		return render(request, template_name, context)

@has_premission()
def remove_practice_page(request, doctor_id, id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		practice = Practice.objects.get(id=id)
	except Practice.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	try:
		doc = practice.doctors.all().get(id=doctor.id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	practice.delete()
	return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))

@has_premission()
def remove_education_page(request, doctor_id, id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		education = Education.objects.get(id=id)
	except Education.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	if education.doctor.id == doctor.id:
		education.delete()
	return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))

@has_premission()
def remove_certificate_page(request, doctor_id, id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		certificate = Certificate.objects.get(id=id)
	except Certificate.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	if certificate.doctor.id == doctor.id:
		certificate.delete()
	return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))

@has_premission()
def edit_certificate_page(request, doctor_id, id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Изменить сертификат'
	context['label'] = 'Сертификат'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		certificate = Certificate.objects.get(id=id)
	except Certificate.DoesNotExist:
		return HttpResponseRedirect(reverse('doctorr_url', kwargs={'id': doctor.id}))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			certificate.name = form.cleaned_data['name']
			certificate.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			context['default_value'] = request.POST['name']
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		context['default_value'] = certificate.name
		return render(request, template_name, context)

@has_premission()
def new_certificate_page(request, doctor_id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Добавить сертификат'
	context['label'] = 'Сертфикат'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			certificate = Certificate()
			certificate.doctor = doctor
			certificate.name = form.cleaned_data['name']
			certificate.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		return render(request, template_name, context)

@has_premission()
def activate_doctor_page(request, id):
	try:
		doctor = Doctor.objects.get(id=id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if doctor.is_active:
		doctor.is_active = False
	else:
		doctor.is_active = True
	doctor.save()
	return HttpResponseRedirect(reverse('doctors_url') + '#' + str(doctor.id))

@has_premission()
def remove_doctor_type_page(request, doctor_id, id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		type = Doctors_type.objects.get(id=id)
	except Doctors_type.DoesNotExist:
		return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
	if type.doctor.id == doctor.id:
		type.delete()
	return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))

@has_premission()
def new_doctor_type_page(request, doctor_id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Добавить тип'
	context['label'] = 'Тип'
	template_name = 'doctors/new_text_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			type = Doctors_type()
			type.doctor = doctor
			type.name = form.cleaned_data['name']
			type.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = TextForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = TextForm()
		return render(request, template_name, context)

@has_premission()
def edit_image_doctor_page(request, doctor_id):
	context = {}
	context['doctor_id'] = doctor_id
	context['header'] = 'Изменить изображение'
	context['label'] = 'Изображение'
	template_name = 'doctors/new_image_form_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			doctor.photo = form.cleaned_data['image']
			doctor.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['form'] = ImageForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = ImageForm()
		return render(request, template_name, context)

@has_premission()
def doctor_move_up_page(request, doctor_id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	doctors = Doctor.objects.filter(number__lte=doctor.number).order_by('-number')
	if doctors.count() > 1:
		one = doctors[0]
		two = doctors[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('doctors_url') + '#' + str(doctor.id))

@has_premission()
def doctor_move_down_page(request, doctor_id):
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	doctors = Doctor.objects.filter(number__gte=doctor.number).order_by('number')
	if doctors.count() > 1:
		one = doctors[0]
		two = doctors[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('doctors_url') + '#' + str(doctor.id))

@has_premission()
def remove_service_for_doctor_page(request, doctor_id, id):
	context = {}
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	try:
		service = Service.objects.get(id=doctor_id)
	except Service.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	doctor.services.remove(service)
	doctor.save()
	return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))

@has_premission()
def new_service_for_doctor_page(request, doctor_id):
	context = {}
	template_name = 'doctors/new_service_for_doctor_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	context['doctor_id'] = doctor.id
	context['form'] = SelectServiceForm(instance=doctor)
	if Service.objects.count() == 0:
		context['error'] = True
		context['error_message'] = 'Список услуг пуст.'
		return render(request, template_name, context)
	# context['form'].fields['services'].required = False
	if request.method == 'POST':
		form = SelectServiceForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data['services'])
			doctor.services.set(form.cleaned_data['services'])
			doctor.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.\n' + str(form.errors)
			return render(request, template_name, context)
	else:
		return render(request, template_name, context)

@has_premission()
def new_technology_for_doctor_page(request, doctor_id):
	context = {}
	template_name = 'doctors/new_technology_for_doctor_page.html'
	try:
		doctor = Doctor.objects.get(id=doctor_id)
	except Doctor.DoesNotExist:
		return HttpResponseRedirect(reverse('doctors_url'))
	context['doctor_id'] = doctor.id
	context['form'] = SelectTechnologyForm(instance=doctor)
	if Technology.objects.count() == 0:
		context['error'] = True
		context['error_message'] = 'Список технологий пуст.'
		return render(request, template_name, context)
	if request.method == 'POST':
		form = SelectTechnologyForm(request.POST)
		if form.is_valid():
			doctor.technologies.set(form.cleaned_data['technologies'])
			doctor.save()
			return HttpResponseRedirect(reverse('doctor_url', kwargs={'id': doctor.id}))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.\n' + str(form.errors)
			return render(request, template_name, context)
	else:
		return render(request, template_name, context)
