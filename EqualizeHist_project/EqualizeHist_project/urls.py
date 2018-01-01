"""EqualizeHist_project URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from EqualizeHist_app import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.HomePage.as_view(), name='index'),
    path(r'upload/', views.upload_image, name='upload'),
    path(r'upload/success/', views.SuccessPage.as_view(), name='upload_success'),
    path(r'upload_success/not_equalized', views.display_histogram, name='notEqualized'),
    path(r'download/', views.download, name='download'),
    path(r'equalize/', views.equalize_histogram, name='equalize'),
    path(r'compare/', views.compare_images, name='compare')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
