"""api_dggs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework import routers

from api_dggs.api.views import BoundaryDatasetsView, BoundaryView

router = routers.DefaultRouter()

router.register(r'bdatasets', BoundaryDatasetsView, basename='bdatasets')
router.register(r'bdatasets/(?P<bds>\w+)', BoundaryDatasetsView, basename='bdatasets')
router.register(r'boundaries', BoundaryView, basename='boundaries')
urlpatterns = router.urls
