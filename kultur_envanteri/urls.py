"""kultur_envanteri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from envanter.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('giris/', giris, name="giris"),
    path('kayit/', kayit, name="kayit"),
    path('cikis/', cikis, name="cikis"),
    path('il/<int:id>', ile_gore_listele, name="ilegore"),
    path('tur/<int:id>', ture_gore_listele, name="turegore"),
    path('ekle/', ekle, name="ekle"),
    path('detay/<int:id>', detay, name="detay"),
    path('ara/', search, name="ara")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
