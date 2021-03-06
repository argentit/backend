from django.db import models
from django import forms
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageCropField, ImageRatioField

class HomePost(models.Model):
	title = models.CharField(max_length = 500, default = '')
	text = models.CharField(max_length = 5000, default = '')
	url = models.URLField(default = None, null=True)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)
	class Meta:
		ordering = ['-datetime']
	def __str__(self):
		return self.title

class Sale(models.Model):
	title = models.CharField(max_length=1000, default='')
	content = RichTextUploadingField(blank=True, null=True)
	# description = models.CharField(max_length=10000, default='')
	datetime = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='img/sales/', default='img/sales/default.jpg', blank=False)
	class Meta:
		ordering = ['-datetime']
	def __str__(self):
		return self.title

class CarouselElement(models.Model):
	title = models.CharField(max_length = 500, default='', null=True, blank=True)
	text = models.CharField(max_length = 5000, default='', null=True, blank=True)
	image = models.ImageField(upload_to='img/home_page/', default='img/home_page/default.jpg', blank=False)
	cropping = ImageRatioField('image', '800x200', hide_image_field=True)
	post = models.ForeignKey(HomePost, on_delete=models.CASCADE, blank=True, null=True, default=None)
	sale = models.ForeignKey(Sale, on_delete=models.CASCADE, blank=True, null=True, default=None)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)
	number = models.CharField(max_length=10, default='0')
	location = models.CharField(max_length=50, default='home')
	class Meta:
		ordering = ['number']

class Practice(models.Model):
	name = models.CharField(max_length = 500, default = '')

class Service(models.Model):
	slug = models.SlugField(max_length = 20, default = '')
	icon = models.ImageField(upload_to='img/service_icons/', default='img/service_icons/default.jpg')
	name = models.CharField(max_length = 500, default = '')
	description = models.CharField(max_length = 10000, default = '')
	price = models.CharField(max_length = 1000, default = '')
	text = models.TextField(default='')
	type = models.TextField(default='', null=True, blank=True)
	def __str__(self):
		return self.name

class SubService(models.Model):
	# type = models.TextField(default='')
	name = models.CharField(max_length = 500, default = '')
	# text = models.TextField(default = '')
	price = models.CharField(max_length = 1000, default = '')
	service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='sub_service', default=None, null=True)

class Technology(models.Model):
	cropping = ImageRatioField('img', '500x500', hide_image_field=True)
	name = models.CharField(max_length = 500, default = '')
	slug = models.SlugField(blank=True, max_length = 20, default = '')
	img = models.ImageField(upload_to='img/technologies/', default='img/technologies/default.jpg')
	text = models.TextField(max_length = 10000000,default='')
	def __str__(self):
		return self.name
	def get_cropping_as_list(self):
		if self.cropping:
			return list(map(int, self.cropping.split(',')))

class Doctor(models.Model):
	name = models.CharField(max_length = 20, default = '')
	surname = models.CharField(max_length = 20, default = '')
	patronymic = models.CharField(max_length = 20, default = '')
	exp = models.DateField(auto_now = False, auto_now_add = False, default = '')
	practice = models.ManyToManyField(Practice, related_name='doctors', default=None)
	slug = models.SlugField(max_length = 20, default = '')
	photo = models.ImageField(upload_to='img/doctors/', default='img/doctors/default.jpg')
	services = models.ManyToManyField(Service, related_name='doctors', default=None, blank=True)
	technologies = models.ManyToManyField(Technology, related_name='doctors', default=None, blank=True)
	is_active = models.BooleanField(default=False)
	number = models.CharField(max_length=10, default='0')
	def __str__(self):
		return self.surname + ' ' + self.name + ' ' + self.patronymic
	class Meta:
		ordering = ['number']

class Doctors_type(models.Model):
	name = models.CharField(max_length = 500, default = '')
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='types', default=None, null=True)

class Skill(models.Model):
	name = name = models.CharField(max_length = 1000, default = '')
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='skills', default=None, null=True)

class Education(models.Model):
	name = models.CharField(max_length = 1000, default = '')
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='education', default=None, null=True)


class Certificate(models.Model):
	doctor = models.ForeignKey(Doctor, related_name='certificates', on_delete=models.CASCADE, default=None, null=True)
	name = models.CharField(max_length=1000, default='')
	class Meta:
		ordering = ['-id']

class Article(models.Model):
	title = models.CharField(max_length = 500, default = '')
	content = RichTextUploadingField(blank=True, null=True)
	datetime = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-datetime']

class Result(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='results', blank=True)
	img_before = models.ImageField(upload_to='img/results/', default='img/results/default.jpg')
	img_after = models.ImageField(upload_to='img/results/', default='img/results/default.jpg')
	text = models.TextField(default='')

class Charity(models.Model):
	img = models.ImageField(upload_to='img/charity/', default='img/charity/default.jpg')
	text = models.CharField(max_length=10000, default='')
	datetime = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-datetime']

class Job(models.Model):
	name = models.CharField(max_length=500, default='')
	description = models.CharField(max_length=10000, default='')

class Document(models.Model):
	name = models.CharField(max_length=500, default='')
	type = models.CharField(max_length=500, default='', blank=True)
	file = models.FileField(upload_to='documents/')

class DMS(models.Model):
	name = models.CharField(max_length=500, default='')
	url = models.URLField(default = None, null=True, blank=True)
	image = models.ImageField(upload_to='img/dms/', default=None, null=True, blank=True)

class Partner(models.Model):
	name = models.CharField(max_length=500, default='')
	url = models.URLField(default = None, null=True, blank=True)
	image = models.ImageField(upload_to='img/partners/', default=None, null=True, blank=True)

class Text(models.Model):
	rich_text = RichTextUploadingField(blank=True, null=True)

	text = models.TextField(default='',blank=True)
	name = models.CharField(max_length=500, default='')
	def __str__(self):
		return self.rich_text

class ImageText(models.Model):
	name = models.CharField(max_length=500, default='', blank=True)
	text = models.TextField(default='')
	url = models.URLField(default=None, null=True, blank=True)
	image = models.ImageField(upload_to='img/iamge_text/', default=None, null=True, blank=True)
	type = models.CharField(max_length=500, default='', blank=True)
	content = RichTextUploadingField(blank=True, null=True, config_name='home')
	datetime = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-id']

class Portal(models.Model):
	name = models.CharField(max_length=500, default='')
	url = models.URLField(default = None, null=True, blank=True)
	image = models.ImageField(upload_to='img/comments/', default='img/comments/default.jpg', blank=True)
	cropping = ImageRatioField('image', '600x200', hide_image_field=True)

class PageMetaData(models.Model):
	url = models.URLField(default = None, null=True, blank=True)
	title = models.CharField(max_length=500, default='', blank=True)
	description = models.CharField(max_length=1000, default='', blank=True)
	keywords = models.CharField(max_length=1000, default='', blank=True)
