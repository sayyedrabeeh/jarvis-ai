from django.urls import path
from .views import process_command,home

urlpatterns = [
    path("process_command/", process_command, name="process_command"),
    path("",home, name="home"),
 
]
