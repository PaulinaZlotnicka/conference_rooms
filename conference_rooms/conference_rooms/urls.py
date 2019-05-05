"""conference_rooms URL Configuration

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
from django.urls import path, re_path
from conf_room_manager.views import AddRoom, EditRoom, DelRoom, ShowOneRoom, ShowRooms, MakeReservation, SearchRooms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new/', AddRoom.as_view()),
    re_path(r'^room/modify/(?P<room_id>\d+)$', EditRoom.as_view()),
    re_path(r'^room/(?P<room_id>\d+)$', ShowOneRoom.as_view()),
    re_path(r'^room/delete/(?P<room_id>\d+)$', DelRoom.as_view()),
    path('room/', ShowRooms.as_view()),
    re_path(r'^reservation/(?P<room_id>\d+)$', MakeReservation.as_view()),
    path('search/', SearchRooms.as_view()),
]


'''
Stwórz URL-e z następującymi funkcjonalnościami do zarządzania salami:

    Tworzenie formularza do stworzenia nowej sali ( /room/new).
    Tworzenie nowej sali ( POST formularza na adres /room/new).
    Tworzenie formularza do modyfikacji sali ( /room/modify/{id}).
    Modyfikacja sali ( POST formularza na adres /room/modify/{id}).
    Usunięcie podanej sali ( /room/delete/{id}).
    Pokazanie danych jednej sali ( /room/{id}).
    Pokazanie wszystkich sal ( adres /).

'''