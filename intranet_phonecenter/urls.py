"""intranet_phonecenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.enable_nav_sidebar = False

import users
import customer
import credits
import calls
import supports

urlpatterns = [
    path(r'users/', include('users.urls', namespace='users')),
    path(r'customer/', include('customer.urls', namespace='customer')),
    path(r'credits/', include('credits.urls', namespace='credits')),
    path(r'calls/', include('calls.urls', namespace='calls')),
    path(r'supports/', include('supports.urls', namespace='supports')),
    path('', users.views.login_view),
    path(r'admin/', admin.site.urls),
    path(r'summernote/', include('django_summernote.urls')),
    # Version bourrine
    # re_path(r'^.*$', users.views.login_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


