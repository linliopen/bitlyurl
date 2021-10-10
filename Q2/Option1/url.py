from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^newurl', views.addShortUrl, name='addShortUrl'),   #POST url  /newurl
    url(r'^([a-zA-Z0-9]{9})', views.url, name='url'), #GET url /[a-zA-Z0-9]{9} match RegEx
]