from playwright.sync_api import expect
from app.test.test_e2e.base import BaseE2ETest
from app.models import User, Event, Venue, Ticket

import datetime
from django.utils import timezone

class EventDetailTest(BaseE2ETest):
    """Test E2E que verifica que un organizador ve la sección de entradas vendidas y el mensaje de la demanda"""

    def setUp(self):
        super().setUp()
        self.organizer = User.objects.create_user(
            username="organizer",
            password="password123",
            is_organizer=True
        )

        self.not_organizer = User.objects.create_user(
            username="not_organizer",
            password="password123",
            is_organizer=True
        )

        self.regular= User.objects.create_user(
            username="regular",
            password="password123",
            is_organizer=False
        )

        self.venue_mocked = Venue.objects.create(
            name='Auditorio UTN',
            address='Av. Siempreviva 742',
            capacity=200
        )

        self.event_mocked = Event.objects.create(
            title="Evento 1",
            description="Descripción del evento 1",
            scheduled_at=timezone.now() + datetime.timedelta(days=1),
            organizer=self.organizer,
            venue=self.venue_mocked
        )

    def test_regular_user_does_not_see_tickest_info_and_demand(self):
        Ticket.objects.create(user=self.regular, event=self.event_mocked, quantity=1, type="general")

        self.login_user("regular","password123")
        self.page.goto(f"{self.live_server_url}/events/")
        self.page.get_by_role("link", name="Ver detalle").first.click()
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.pk}/")
        expect(self.page.get_by_text("Entradas vendidas:")).not_to_be_visible()
        expect(self.page.get_by_text("Demanda:")).not_to_be_visible()

    def test_organizer_sees_high_demand(self):
        Ticket.objects.create(user=self.regular, event=self.event_mocked, quantity=190, type="general")

        self.login_user("organizer","password123")
        self.page.goto(f"{self.live_server_url}/my_events/")
        self.page.get_by_role("link", name="Ver detalle").first.click()
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.pk}/")

        expect(self.page.get_by_text("Entradas vendidas: 190")).to_be_visible()
        expect(self.page.get_by_text("Demanda: ALTA")).to_be_visible()

    def test_organizer_sees_low_demand(self):
        Ticket.objects.create(user=self.regular, event=self.event_mocked, quantity=1, type="general")

        self.login_user("organizer","password123")
        self.page.goto(f"{self.live_server_url}/my_events/")
        self.page.get_by_role("link", name="Ver detalle").first.click()
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.pk}/")

        expect(self.page.get_by_text("Entradas vendidas: 1")).to_be_visible()
        expect(self.page.get_by_text("Demanda: BAJA")).to_be_visible()

    def test_organizer_sees_medium_demand(self):
        Ticket.objects.create(user=self.regular, event=self.event_mocked, quantity=40, type="general")

        self.login_user("organizer","password123")
        self.page.goto(f"{self.live_server_url}/my_events/")
        self.page.get_by_role("link", name="Ver detalle").first.click()
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.pk}/")

        expect(self.page.get_by_text("Entradas vendidas: 40")).to_be_visible()
        expect(self.page.get_by_text("Demanda: MEDIA")).to_be_visible()
        
        





