from django.http import HttpResponse
from django.conf import settings
from django.http import Http404

def robots_txt(request):
	try:
		path = settings.BASE_DIR + '/../robots.txt'
		file = open(path, 'r')
		content = file.read()
		return HttpResponse(content, content_type='text/plain')
	except Exception as e:
		print(e)
		return HttpResponse(content_type='text/plain')

def return404(request):
	raise Http404
