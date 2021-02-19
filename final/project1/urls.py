"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from core import views as core_views
from programs import views as program_views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'programs', program_views.ProgramViewSet)
router.register(r'users', program_views.UserViewSet)
router.register(r'program-categories', program_views.CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('programs/', program_views.programs, name='programs'),
    path('programs/add/', program_views.add, name='programs_add'),
    path('programs/edit/<int:id>/', program_views.edit, name='programs_edit'),
    path('about/', core_views.about, name='about'),
    path('login/', core_views.login, name='login'),
    path('logout/', core_views.logout, name='logout'),
    path('join/', core_views.join, name='join'),
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework'))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
