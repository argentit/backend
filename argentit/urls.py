from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^select2/', include('django_select2.urls')),
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
	path('', include('alfa.urls')),
	# url(r'', RedirectView.as_view(pattern_name='home_url', permanent=False))
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
