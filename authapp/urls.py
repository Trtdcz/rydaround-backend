from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register(r'registration', views.UserRegisterViewSet,basename='user-registeration'),

urlpatterns=[
    path('', include(router.urls)),
    
    #   Basic API's
    path('login/', obtain_auth_token),
    path('logout/', views.LogoutAPIView.as_view()),
    
    # APIs for Ticket
    path('tickets/', views.TicketsAPIView.as_view()),
    path('tickets/<int:pk>/', views.TicketsAPIView.as_view()),
    path('ticket_detail/<int:pk>/', views.TicketDetailAPIView.as_view()),

    # User API's
    path('user_tickets_list/<int:pk>/', views.UserTicketListAPIView.as_view()),
    path('user_info_by_departure_airport_and_check_in_status/<str:departure_airport>/<str:check_in_status>/', views.GetUserAndFlightInfoByDepartureAirportAndCheckInStatusView.as_view()),
]


