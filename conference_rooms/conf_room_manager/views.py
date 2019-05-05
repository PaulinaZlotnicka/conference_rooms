from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse
from conf_room_manager.models import Room, RoomReservation
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import datetime
from dateutil import parser

class AddRoom(View):
    def get(self, request):
        ctx = {"text": "Podaj dane nowej sali:",
               "title": "DODANIE SALI"
        }
        return render(request, "add_room.html", ctx)

    def post(self,request):
        if request.POST.get('new_room'):
            try:
                Room.objects.get(name=str(request.POST.get('name')))
            except ObjectDoesNotExist:
                Room.objects.create(name=str(request.POST.get('name')), capacity=int(request.POST.get('capacity')),
                                    projector_available=bool(request.POST.get('projector_available')), air_conditioned=bool(request.POST.get('air_conditioned')))
                ctx = {"text": "Dodana sala o nazwie {}".format(str(request.POST.get('name'))),
                       "title": "DODANIE SALI"
                       }
            else:
                ctx = {"text": "TA SALA JEST JUŻ W NASZEJ BAZIE",
                       "title": "DODANIE SALI"
                       }
        return render(request, "add_room.html", ctx)

class EditRoom(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        ctx = {"room": room,
               "title": "ZMIANA DANYCH"}
        return render(request, "edit_room.html", ctx)

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        if request.POST.get('name_change'):
            room.name = str(request.POST.get('name'))
        if request.POST.get('capacity_change'):
            room.capacity = int(request.POST.get('capacity'))
        if request.POST.get('projector_available_change'):
            room.projector_available = bool(request.POST.get('projector_available'))
        if request.POST.get('air_conditioned_change'):
            room.air_conditioned = bool(request.POST.get('air_conditioned'))
        room.save()

        ctx = {"room": room,
               "text": "ZMIANA DANYCH POWIODŁA SIĘ",
               "title": "ZMIANA DANYCH"
               }
        return render(request, "edit_room.html", ctx)

class DelRoom(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        ctx = {"room": room,
               'text': "NAZWA SALI {}".format(room.name),
               "title": "USUNIĘCIE DANYCH"}
        return render(request, "del_room.html", ctx)

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        if request.POST.get('del_room'):
            room.delete()
        ctx = {
               "text": "USUNIĘCIE SALI POWIODŁO SIE",
               "title": "USUNIĘCIE DANYCH"
               }
        return render(request, "del_room.html", ctx)

class ShowOneRoom(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        ctx = {"room": room,
               "title": "DANE SALI"}
        return render(request, "show_one_room.html", ctx)

class ShowRooms(View):
    def get(self, request):
        rooms_list = Room.objects.all()
        for room in rooms_list:
            try:
                RoomReservation.objects.filter(date=datetime.datetime.now().date()).filter(room=room)
            except ObjectDoesNotExist:
                available = "DZIŚ WOLNA"
            else:
                available = "DZIŚ ZAJĘTA"

        ctx = {"rooms_list": rooms_list,
               "available": available,
               "title": "SALE"}
        return render(request, 'rooms.html', ctx)

    def post(self, request):
        rooms_list = Room.objects.all()
        ctx = {"rooms_list": rooms_list,
               "title": "SALE"}
        return render(request, 'rooms.html', ctx)

class MakeReservation(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        ctx = {"room": room,
               "title": "REZERWACJA"}
        return render(request, "make_reservation.html", ctx)

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        min_date = datetime.datetime.now().date()
        if request.POST.get('make_reservation'):
            res_date = parser.parse(request.POST.get('res_date')).date()
            if res_date > min_date:
                try:
                    RoomReservation.objects.get(date=parser.parse(request.POST.get('res_date')).date())
                except ObjectDoesNotExist:
                    RoomReservation.objects.create(date=parser.parse(request.POST.get('res_date')).date(), room=room,
                                                   comment=request.POST.get('comment'))
                    ctx = {"text": "Zarezerwowana sala {} na dzień {}".format(room.name, parser.parse(request.POST.get('res_date')).date()),
                           "title": "REZERWACJA"
                           }
                else:
                    ctx = {"text": "SALA NIE JEST DOSTĘPNA",
                           "title": "REZERWACJA"
                           }
            else:
                ctx = {"text": "WYBIERZ POPRAWNĄ DATĘ",
                       "title": "REZERWACJA"
                       }
            return render(request, "make_reservation.html", ctx)

class SearchRooms(View):
    def get(self, request):
        ctx = {"text_1": "Wypełnij kryteria wyszukiwania:",
               "title": "SZUKANIE SALI"
        }
        return render(request, "search_rooms.html", ctx)

    def post(self, request):
        rooms_list=[]
        if request.POST.get("search_name"):
            rooms_list = Room.objects.filter(name__contains=request.POST.get('name'))
        if request.POST.get("search_capacity"):
            rooms_list = Room.objects.filter(capacity__gte=int(request.POST.get("capacity")))
        if request.POST.get("search_projector"):
            rooms_list = Room.objects.filter(projector_available=bool(request.POST.get('projector_available')))
        if request.POST.get("search_ac"):
            rooms_list = Room.objects.filter(air_conditioned=bool(request.POST.get('air_conditioned')))
        if request.POST.get("search_date"):
            rooms_list = RoomReservation.objects.filter(date=parser.parse(request.POST.get("date")))

        ctx = {"rooms_list": rooms_list,
                "text_2": "WYNIK WYSZUKIWANIA:",
               "title": "SZUKANIE SALI"
        }
        return render(request, "search_rooms.html", ctx)
        
