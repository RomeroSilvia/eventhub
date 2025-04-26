from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("/", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/login/", views.login_view, name="login"),
    path("events/", views.events, name="events"),
    path("events/create/", views.event_form, name="event_form"),
    path("events/<int:id>/edit/", views.event_form, name="event_edit"),
    path("events/<int:id>/", views.event_detail, name="event_detail"),
    path("events/<int:id>/delete/", views.event_delete, name="event_delete"),
    path('events/<int:event_id>/buy-ticket/', views.buy_ticket, name='buy_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]
