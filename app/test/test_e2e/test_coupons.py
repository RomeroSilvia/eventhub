import datetime
from django.utils import timezone
from playwright.sync_api import expect
from app.models import Event, User, Venue, Coupon, Ticket
from app.test.test_e2e.base import BaseE2ETest
from django.urls import reverse


def assert_input_value_equals(locator, expected_value: str):
    actual_value = locator.input_value().replace(",", ".")
    assert actual_value == expected_value, f"Expected '{expected_value}', got '{actual_value}'"


class CouponBaseTest(BaseE2ETest):
    """Clase base específica para tests de cupones"""

    def setUp(self):
        super().setUp()

        self.mocked_user = User.objects.create_user(username="regular", password="password123", is_organizer=False)
        self.mocked_organizer_user = User.objects.create_user(username="organizador", password="password123", is_organizer=True)
        self.mocked_venue = Venue.objects.create(
            name="Auditorio Nacional",
            address="60 y 124",
            capacity=5000,
            country="ARG",  
            city="La Plata"
        )

        self.event_mocked = Event.objects.create(
            title="Evento de prueba 1",
            description="Descripción del evento 1",
            scheduled_at="2026-12-01T10:00:00Z",
            organizer=self.mocked_organizer_user,
            venue=self.mocked_venue,
            price=50.00
        )
        
        self.mocked_coupon = Coupon.objects.create(
            event=self.event_mocked,
            discount_percent=10,
            expiration_date="2026-12-01T10:00:00Z",
            organizer=self.mocked_organizer_user
        )



class CouponDisplayTest(CouponBaseTest):
    """Tests de visualización de cupones para el organizador"""
    def test_coupons_page_display_as_organizer(self):
        
        self.page.goto(f"{self.live_server_url}/accounts/login/")
        self.page.fill("input[name='username']", "organizador")
        self.page.fill("input[name='password']", "password123")
        self.page.click("button[type='submit']")
        self.page.wait_for_load_state("networkidle")
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.id}/coupons/")
     
        header = self.page.locator("h1.h4.mb-0")
        expect(header).to_have_text(f'Cupones para "{self.event_mocked.title}"')
        
        table = self.page.locator("table.table")
        expect(table).to_be_visible()

        crear_btn = self.page.locator("a.btn.btn-primary", has_text="Crear Cupón")
        expect(crear_btn).to_be_visible()

class CouponCreateTest(CouponBaseTest):
    """Tests de creación de cupones"""
    def test_create_coupon_as_organizer(self):
        self.page.goto(f"{self.live_server_url}/accounts/login/")
        self.page.fill("input[name='username']", "organizador")
        self.page.fill("input[name='password']", "password123")
        self.page.click("button[type='submit']")
        self.page.wait_for_load_state("networkidle")
        self.page.goto(f"{self.live_server_url}/events/{self.event_mocked.id}/coupons/create/")

        header = self.page.locator("h1")
        expect(header).to_have_text(f'Crear Cupón para "{self.event_mocked.title}"')
        
        discount_label=self.page.locator("label[for='discount_percentage']")
        expect(discount_label).to_have_text("Porcentaje de Descuento *")
        
        expiration_label = self.page.locator("label[for='expiration_date']")
        expect(expiration_label).to_have_text("Fecha de Expiración *")
        
        discount_input = self.page.locator("input#discount_percentage")
        expiration_input = self.page.locator("input#expiration_date")
        
        discount_input.fill("15")
        expiration_input.fill("2026-12-31T23:59")

        submit_btn = self.page.locator("button[type='submit'].btn-primary")
        submit_btn.click()

        expect(self.page).to_have_url(f"{self.live_server_url}/events/{self.event_mocked.id}/coupons/")

        discount_column = self.page.locator("table td", has_text="15%")
        expect(discount_column).to_be_visible()