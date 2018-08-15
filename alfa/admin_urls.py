from django.urls import path
from django.conf.urls import url
from django.conf.urls import include

from alfa.views import admin_views, charity, jobs, news, for_patients, info, service, doctors, technologies, results

urlpatterns = [
				url(r'^login/$', admin_views.admin_auth_page, name = 'admin_auth_url'),
				url(r'^logout/$', admin_views.logout_page, name = 'logout_url'),
				url(r'^doctors/new/$', doctors.new_doctor_page, name = 'new_doctor_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/certificate/new/$', doctors.new_certificate_page, name = 'new_certificate_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/certificate/remove/(?P<id>\d+)$', doctors.remove_certificate_page, name = 'remove_certificate_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/certificate/edit/(?P<id>\d+)$', doctors.edit_certificate_page, name = 'edit_certificate_url'),

				url(r'^doctors/(?P<doctor_id>\d+)/education/new/$', doctors.new_education_page, name = 'new_education_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/education/remove/(?P<id>\d+)$', doctors.remove_education_page, name = 'remove_education_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/education/edit/(?P<id>\d+)$', doctors.edit_education_page, name = 'edit_education_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/practice/edit/(?P<id>\d+)$', doctors.edit_practice_page, name = 'edit_practice_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/practice/remove/(?P<id>\d+)$', doctors.remove_practice_page, name = 'remove_practice_url'),
				url(r'^doctors/(?P<doctor_id>\d+)/practice/new/$', doctors.new_practice_page, name = 'new_practice_url'),
				url(r'^doctors/edit/(?P<id>\d+)$', doctors.edit_doctor_page, name = 'edit_doctor_url'),
				url(r'^doctors/remove/(?P<id>\d+)$', doctors.remove_doctor_page, name = 'remove_doctor_url'),
				url(r'^technologies/new/$', technologies.new_technology_page, name = 'new_technology_url'),
				url(r'^technologies/remove/(?P<id>\d+)$', technologies.remove_technology_page, name = 'remove_technology_url'),
				url(r'^technologies/edit/(?P<id>\d+)$', technologies.edit_technology_page, name = 'edit_technology_url'),
				url(r'^service/new/$', service.new_service_page, name = 'new_service_url'),
				url(r'^service/remove/(?P<id>\d+)$', service.remove_service_page, name = 'remove_service_url'),
				url(r'^news/new/$', news.new_news_page, name = 'new_news_url'),
				url(r'^news/edit/(?P<id>\d+)$', news.edit_news_page, name = 'edit_news_url'),
				url(r'^news/remove/(?P<id>\d+)$', news.remove_news_page, name = 'remove_news_url'),
				url(r'^results/new/$', results.new_result_page, name = 'new_result_url'),
				url(r'^results/remove/(?P<id>\d+)$', results.remove_result_page, name = 'remove_result_url'),
				url(r'^home/new$', admin_views.new_home_item_page, name = 'new_home_item_url'),
				url(r'^charity/new$', charity.new_charity_page, name = 'new_charity_url'),
				url(r'^charity/remove/(?P<id>\d+)$', charity.remove_charity_page, name = 'remove_charity_url'),
				url(r'^charity/edit/(?P<id>\d+)$', charity.edit_charity_page, name = 'edit_charity_url'),
				url(r'^info/new$', info.new_info_page, name = 'new_info_url'),
				url(r'^info/edit/(?P<id>\d+)$', info.edit_info_page, name = 'edit_info_url'),
				url(r'^info/remove/(?P<id>\d+)$', info.remove_info_page, name = 'remove_info_url'),
				url(r'^jobs/new$', jobs.new_job_page, name = 'new_job_url'),
				url(r'^jobs/edit/(?P<id>\d+)$', jobs.edit_job_page, name = 'edit_job_url'),
				url(r'^jobs/remove/(?P<id>\d+)$', jobs.remove_job_page, name = 'remove_job_url'),
				url(r'^for_patients/new$', for_patients.new_for_patients_page, name = 'new_for_patients_url'),
				]
