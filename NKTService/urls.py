"""NKTService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from base.views import order_list_in_work

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('base.urls')),
    path('profile/', include('additional_user.urls')),
    path('serials/', include('serials.urls')),
    path('accompanying_sheets/', include('accompanying_sheets.urls')),
    path('warrantycards/', include('warrantycards.urls')),
    path('autocomplete/', include('autocomplete.urls')),

    path('', order_list_in_work),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', LoginView.as_view(template_name='registration/login.html'), name='login'),
]

#urlpatterns += staticfiles_urlpatterns()

#When in development mode and when you are using some other server for local development add this to your url.py
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()
#When in production you never, ever put gunicorn in front. Instead you use a server like nginx which dispatches requests to a pool of gunicorn workers and also serves the static files.
#http://gunicorn.org/deploy.html