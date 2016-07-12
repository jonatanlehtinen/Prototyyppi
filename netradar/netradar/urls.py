"""netradar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from paja import views

urlpatterns = [
#    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^pong/', views.pong),
    url(r'^soc/', include("social.apps.django_app.urls", namespace="social")),
    url(r'^mydata/', views.mydata_view),
    url(r'^login/', views.login),
    url(r'^register/', views.register_view),
#    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'', include('social_auth.urls')),
]
