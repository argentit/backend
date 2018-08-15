from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *


def comments_page(request):
	context = {}

	return render(request, 'comments/comments_page.html', context)
