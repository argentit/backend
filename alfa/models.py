from django.db import models
from django import forms
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Doctors_type(models.Model):
	name = models.CharField(max_length = 50, default = '')

class Practice(models.Model):
	name = models.CharField(max_length = 500, default = '')

class Service(models.Model):
	slug = models.SlugField(max_length = 20, default = '')
	icon = models.ImageField(upload_to='img/service_icons/', default='img/service_icons/default.jpg')
	name = models.CharField(max_length = 50, default = '')
	description = models.CharField(max_length = 10000, default = '')
	price = models.CharField(max_length = 1000, default = '')
	text = models.TextField(default='')

class Technology(models.Model):
	name = models.CharField(max_length = 20, default = '')
	slug = models.SlugField(max_length = 20, default = '')
	img = models.ImageField(upload_to='img/technologies/', default='img/technologies/default.jpg')
	text = models.TextField(default='')

class Doctor(models.Model):
	name = models.CharField(max_length = 20, default = '')
	surname = models.CharField(max_length = 20, default = '')
	patronymic = models.CharField(max_length = 20, default = '')
	type = models.ManyToManyField(Doctors_type, default=None, related_name='doctors')
	exp = models.DateField(auto_now = False, auto_now_add = False, default = '')
	practice = models.ManyToManyField(Practice, related_name='doctors', default=None)
	slug = models.SlugField(max_length = 20, default = '')
	photo = models.ImageField(upload_to='img/doctors/', default='img/doctors/default.jpg')
	services = models.ManyToManyField(Service, related_name='doctors', default=None)
	technologies = models.ManyToManyField(Technology, related_name='doctors', default=None)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		return self.name + ' ' + self.surname + ' ' + self.patronymic

class Skill(models.Model):
	name = name = models.CharField(max_length = 1000, default = '')
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='skills', default=None, null=True)

class Education(models.Model):
	name = models.CharField(max_length = 1000, default = '')
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='education', default=None, null=True)


class Certificate(models.Model):
	doctor = models.ForeignKey(Doctor, related_name='certificates', on_delete=models.CASCADE, default=None, null=True)
	name = models.CharField(max_length=200, default='')

class Article(models.Model):
	title = models.CharField(max_length = 100, default = '')
	content = RichTextUploadingField(blank=True, null=True)
	date = models.DateField(auto_now=True)
	class Meta:
		ordering = ['-date']

class Result(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='results')
	img_before = models.ImageField(upload_to='img/results/', default='img/results/default.jpg')
	img_after = models.ImageField(upload_to='img/results/', default='img/results/default.jpg')
	text = models.TextField(default='')

class Charity(models.Model):
	img = models.ImageField(upload_to='img/charity/', default='img/charity/default.jpg')
	text = models.CharField(max_length=10000, default='')

class Job(models.Model):
	name = models.CharField(max_length=100, default='')
	description = models.CharField(max_length=10000, default='')

class Document(models.Model):
	name = models.CharField(max_length=100, default='')
	type = models.CharField(max_length=100, default='')
	file = models.FileField(upload_to='documents/')
