from django.contrib import admin
from.models import MyUser, Ticket, TripDetail


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'username', 'password', 'email', 'first_name', 'last_name', 'middle_name', 'additional_email_1', 
		'additional_email_2', 'additional_email_3', 'phone_number', 'additional_phone_number_1', 
		'additional_phone_number_2', 'additional_phone_number_3', 'reference_destination_account', 
		'alias_destination_account', 'current_time', 'current_location',
	)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ['id', 'owner', 'ticket_number', 'airline_name', 'airline_iata_code', 'airline_icao_code', 'flight_number', 'departure_airport', 
	'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'check_in_status', 'check_luggage', 'forecast_provided', 
	'trip_reason', 'time_stamp', 'created_at', 'is_delete']
	list_filter = ['owner', 'airline_name']


@admin.register(TripDetail)
class TripDetailAdmin(admin.ModelAdmin):
	list_display = ['id', 'owner', 'ticket', 'arrival_pickup_location', 'arrival_transfer_type', 'arrival_transfer_status', 'arrival_transfer_booked', 
	'arrival_transfer_eta', 'departure_dropoff_location', 'departure_transfer_type', 'departure_transfer_status', 'departure_transfer_booked', 'created_at']
	list_filter = ['owner', 'ticket']
