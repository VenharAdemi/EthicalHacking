"""
URL configuration for EHProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ethicalHacking import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("comment/", views.comment, name="comment"),
    path("register/", views.register, name="register"),
    path("deserialize/", views.deserialize_data, name="deserialize"),
    path("transfer/", views.transfer_money, name="transfer"),
    path("fetch_data/", views.fetch_data, name="fetch_data"),
    path("login_attempt/", views.login_attempt, name="login_attempt"),
    path("parse_xml/", views.parse_xml, name="parse_xml"),
    path("profile/<int:user_id>/", views.view_profile, name="view_profile"),
]
