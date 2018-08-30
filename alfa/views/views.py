from django.http import HttpResponse

def robots_txt(request):
	content = {}
	return HttpResponse(content_type='text/plain')
