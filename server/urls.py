from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from server import views

admin.autodiscover()

router = routers.DefaultRouter()
#router.register(r'courses', views.Courses)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
)
