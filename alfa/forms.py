from django import forms
from alfa.models import *
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import Select2Widget
from datetime import date


class ResultForm(forms.ModelForm):
	class Meta:
		model = Result
		fields = ['doctor', 'img_before', 'img_after', 'text']
		widgets = {
			'text': forms.widgets.Textarea(attrs={'class': 'form-control rounded-0', 'rows': 4, 'required': ''}),
			'img_before': forms.widgets.FileInput(attrs={'required':''}),
			'img_after': forms.widgets.FileInput(attrs={'required':''}),
			'doctor': forms.widgets.CheckboxSelectMultiple(),
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
		fields = ['name', 'surname', 'patronymic', 'exp', 'photo', ]
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
			'exp': forms.widgets.SelectDateWidget(years=range(1950, date.today().year + 1),attrs={'class': 'form-control rounded-0 col mx-3', 'required': ''},),
			# 'img_before': forms.widgets.FileInput(attrs={'required':''}),
			# 'img_after': forms.widgets.FileInput(attrs={'required':''}),
		}


class NewDoctor(forms.Form):
	name = forms.CharField()
	surname = forms.CharField()
	patronymic = forms.CharField()
	slug = forms.CharField()
	exp = forms.DateField()
	image = forms.ImageField()

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

class DocumentForm(forms.Form):
	name = forms.CharField(required=True)
	file = forms.FileField(required=True)

class JobForm(forms.Form):
	name = forms.CharField(required=True)
	description = forms.CharField(required=True)

class ServiceForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField()
	price = forms.CharField()

class TechnologyForm(forms.Form):
	name = forms.CharField(required=True)
	file = forms.ImageField(required=True)
	description = forms.CharField(required=True)

class TextForm(forms.Form):
	name = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'form-control rounded-0 ', 'required': '', 'rows': '4'}))
