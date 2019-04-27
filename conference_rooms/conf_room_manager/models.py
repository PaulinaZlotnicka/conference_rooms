from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.SmallIntegerField()
    projector_available = models.BooleanField(default=False)
    air_conditioned = models.BooleanField(default=False)

class RoomReservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.CharField(max_length=64)

    class Meta: #klasa meta dla unique together, która po niczym nie dziedziczy, to informacje o modelu RoomReservation
        # managed = False #wtedy migracje nie dotyczą tej klasy
        # table_name = 'Whatever' #jeśli chcę żeby nazwa była inna niz domysnlne nazwa_aplikacji_nazwa_klasy
        unique_together = [['room', 'date']] #lista liast, wpisujemy stringi ktore są nazwami naszych zmiennych, to przeklada się na utworzenie nowej tabeli




