from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase
from app.models import Event, Rating, Venue

User = get_user_model()

class RatingAverageCalculation(TestCase):

    def setUp(self):
        self.mocked_organizer = User.objects.create_user(username="organizer", password="pass")
        self.mocked_user = User.objects.create_user(username="user2", password="pass")
        self.venue_mocked = Venue.objects.create(
            name="Auditorio Nacional",
            address="60 y 124",
            capacity=5000,
            country="ARG",  
            city="La Plata"
        )
        self.mocked_event = Event.objects.create(
            title="Evento Test", 
            description="Test description",
            scheduled_at="2025-12-01T10:00:00Z",
            organizer=self.mocked_organizer, 
            venue=self.venue_mocked
        )

    def test_rating_average_calculation(self):
        Rating.objects.create(
            evento=self.mocked_event, usuario=self.mocked_organizer,
            titulo="Muy Bueno", calificacion=5, texto="El evento estuvo muy interesante"
        )

        Rating.objects.create(
            evento=self.mocked_event, usuario=self.mocked_user,
            titulo="No me intereso", calificacion=3, texto="El evento estuvo bien, pero puede mejorar"
        )

        Rating.objects.create(
            evento=self.mocked_event, usuario=User.objects.create_user(username="user3", password="pass"),
            titulo="Malo", calificacion=1, texto="No me gusto nada"
        )

        self.assertEqual(self.mocked_event.rating_average, 3.0)
    
