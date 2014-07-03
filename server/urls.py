from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from server.views import *

admin.autodiscover()

#router = routers.DefaultRouter()
#router.register(r'courses', views.Courses)
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
#router.register(r'courses', views.CourseViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', landing_page),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),





    url(r'^subjects/$', get_subjects),
    url(r'^schools/$', get_schools),
    url(r'^terms/$', get_terms),
    url(r'^instructors/$', get_instructors),
    url(r'^courses/$', get_courses),
    url(r'^courses/search/$', search_courses),
    url(r'^courses/summary/$', get_courses_summary),




    #url(r'^', include(router.urls)),
)
