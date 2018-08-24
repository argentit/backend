from django import forms
from alfa.models import *
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import Select2Widget
from datetime import date
from image_cropping import ImageCropField, ImageRatioField
from image_cropping import ImageCropWidget

class SelectServiceForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ['services']
		widgets = {
			'services': forms.widgets.CheckboxSelectMultiple(attrs={'class': 'list-unstyled rounded-0',},),
		}
		labels = {
			'services' : 'Услуга:'
		}

class SelectTechnologyForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ['technologies']
		widgets = {
			'technologies': forms.widgets.CheckboxSelectMultiple(attrs={'class': 'list-unstyled rounded-0',},),
		}
		labels = {
			'technologies' : 'Технологии:'
		}


class HomePostForm(forms.ModelForm):
	url = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ',}), label='Ссылка:')
	class Meta:
		model = HomePost
		fields = ['title', 'url', 'text']
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0', 'rows': 5, 'required': ''}),

		}
		labels = {
			'title': 'Заголовок:',
			'url': 'Ссылка:',
			'text': 'Текст:',
		}

class EditCarouselElementForm(forms.ModelForm):
	class Meta:
		model = CarouselElement
		fields = ['title', 'text', 'post', 'image', 'cropping']
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ',}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0', 'rows': 4,}),
			'post': forms.widgets.Select(attrs={'class': 'form-control rounded-0',}),
			'image': ImageCropWidget,
		}
		labels = {
			'title': 'Заголовок (на изображении):',
			'text': 'Текст (на изображении):',
			'post': 'Ссылка:',
			'image': 'Изображение:',
			'cropping': ''
		}

class NewCarouselElementForm(forms.ModelForm):
	class Meta:
		model = CarouselElement
		fields = ['title', 'text', 'post', 'image',]
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ',}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0', 'rows': 4,}),
			'post': forms.widgets.Select(attrs={'class': 'form-control rounded-0',}),
			'image': forms.widgets.FileInput(attrs={'required':''}),
		}
		labels = {
			'title': 'Заголовок (на изображении):',
			'text': 'Текст (на изображении):',
			'post': 'Ссылка:',
			'image': 'Изображение:',
		}

class ResultForm(forms.ModelForm):
	class Meta:
		model = Result
		fields = ['doctor', 'img_before', 'img_after', 'text']
		widgets = {
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0', 'rows': 4, 'required': ''}),
			'img_before': forms.widgets.FileInput(attrs={'required':''}),
			'img_after': forms.widgets.FileInput(attrs={'required':''}),
			'doctor': forms.widgets.Select(attrs={'class':'form-control col-6'}),
		}
		labels = {
			'doctor': 'Доктор:',
			'text': 'Описание:',
			'img_before': 'До:',
			'img_after': 'После:',
		}

class DoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ['surname', 'name', 'patronymic', 'exp', 'photo', ]
		labels = {
			'name': 'Имя:',
			'surname': 'Фамилия:',
			'patronymic': 'Отчество:',
			'exp': 'Дата окончания университета:',
			'photo': 'Изображение:',
		}
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'surname': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'patronymic': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'exp': forms.widgets.SelectDateWidget(years=range(1980, date.today().year + 1),attrs={'class': 'form-control rounded-0 col mx-3', 'required': ''},),
			# 'img_before': forms.widgets.FileInput(attrs={'required':''}),
			# 'img_after': forms.widgets.FileInput(attrs={'required':''}),
		}
class AuthForm(forms.Form):
	login = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class NewsForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title','content']
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class': 'my-2 mp-0 rounded-0', 'style': 'width:100%'}),
		}
		labels = {
			'title': 'Заголовок',
			'content': '',
		}

	def css_classes(str):
		return str

	def as_div(self):
		return self._html_output(
			normal_row='<div%(html_class_attr)s>%(label)s%(errors)s%(field)s%(help_text)s</div>',
			error_row='<tr><td colspan="2">%s</td></tr>',
			row_ender='</td></tr>',
			help_text_html='<br><span class="helptext">%s</span>',
			errors_on_separate_row=False,
		)

class CharityForm(forms.Form):
	img = forms.ImageField(required=True)
	text = forms.CharField(required=True)
	object_id = forms.IntegerField(required=False)

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ['name', 'file',]
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0', 'required': ''}),
			'file': forms.widgets.FileInput(attrs={'required':'', 'accept': '.pdf'}),
		}
		labels = {
			'name': 'Название документа:',
			'file': 'Документ (pdf):',
		}

class JobForm(forms.Form):
	name = forms.CharField(required=True)
	description = forms.CharField(required=True)

class ServiceForm(forms.ModelForm):
	class Meta:
		model = Service
		fields = ['name', 'price', 'text', ]
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'price': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0 ', 'rows': '8', 'required': ''}),

        }
		labels = {
			'name': 'Название:',
			'text': 'Текст',
			'price': 'Цена:',
		}
	# name = forms.CharField()
	# description = forms.CharField()
	# price = forms.CharField()

class TechnologyForm(forms.Form):
	name = forms.CharField(required=True)
	#file = ImageCropField(blank=True, upload_to='uploaded_images')
	description = forms.CharField(required=True)

class EditTechnologyForm(forms.ModelForm):
	class Meta:
		model = Technology
		fields = ['name', 'text', 'img','cropping',]
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0 ', 'rows': '8', 'required': ''}),
            'img': ImageCropWidget,
        }
		labels = {
			'name': 'Название:',
			'text': 'Текст',
			'img': 'Изображение:',
			'cropping': ''
		}

class NewTechnologyForm(forms.ModelForm):
	class Meta:
		model = Technology
		fields = ['name', 'text', 'img',]
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ', 'required': ''}),
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0 ', 'rows': '8', 'required': ''}),
            'img': forms.widgets.FileInput(attrs={'required':''}),
        }
		labels = {
			'name': 'Название:',
			'text': 'Текст',
			'img': 'Изображение:',
		}

class TextForm(forms.Form):
	name = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'form-control rounded-0 ', 'required': '', 'rows': '4'}))

class ImageForm(forms.Form):
	image = forms.ImageField(required=True)

class DMSForm(forms.ModelForm):
	class Meta:
		model = DMS
		fields = ['name', 'url', 'image']
		widgets = {
			'name': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ',}),
			'url': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0 ',}),
            'image': forms.widgets.FileInput(attrs={'accept': 'image/*',}),
        }
		labels = {
			'name': 'Название:',
			'url': 'Ссылка:',
			'image': 'Изображение:',
		}
