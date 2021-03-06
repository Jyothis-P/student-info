"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.static import serve
# from django.urls import
from django.contrib import admin

from django.conf import settings

urlpatterns = [

    # path(r'^student/',)
    #

    url(r'^admin/', admin.site.urls),
    url(r'^student/', include('student.urls')),
    url(r'^faculty/', include('student.f_urls')),

    url(r'^accounts/',include('django.contrib.auth.urls')),

    # url(r'^student/searchs/', include('student.urls')),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),



]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG==True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False

#
# if settings.DEBUG==False:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
