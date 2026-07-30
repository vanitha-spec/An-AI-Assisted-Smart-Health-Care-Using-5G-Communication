from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AccessIOT.html', views.AccessIOT, name="AccessIOT"), 
	       path('AccessIOTAction', views.AccessIOTAction, name="AccessIOTAction"),
	       
]