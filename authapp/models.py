from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class MyUser(AbstractUser):
	"""
	Custom user model inherited from AbstractUser class
	"""
	middle_name = models.CharField(max_length=150)
	additional_email_1 = models.EmailField(null=True, blank=True)
	additional_email_2 = models.EmailField(null=True, blank=True)
	additional_email_3 = models.EmailField(null=True, blank=True)
	phone_number = PhoneNumberField()
	additional_phone_number_1 = PhoneNumberField(blank=True)
	additional_phone_number_2 = PhoneNumberField(blank=True)
	additional_phone_number_3 = PhoneNumberField(blank=True)
	reference_destination_account =  models.EmailField(null=True, blank=True)
	alias_destination_account = models.EmailField(null=True, blank=True)
	current_time = models.DateTimeField(auto_now_add=True)
	current_location = models.CharField(max_length=150)
	
	class Meta:
		db_table = 'table_users'
		verbose_name_plural = 'Users'
		
	def __str__(self):
		return self.email


class Ticket(models.Model):
	"""
	Tickets model for storing the tickets detail
	"""
	owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
	ticket_number = models.CharField(max_length=255, default="", null=True, blank=True)
	airline_name = models.CharField(max_length=255, default="", null=True, blank=True)
	airline_iata_code = models.CharField(max_length=255, default="", null=True, blank=True)
	airline_icao_code = models.CharField(max_length=255, default="", null=True, blank=True)
	flight_number = models.CharField(max_length=255, default="", null=True, blank=True)
	departure_airport = models.CharField(max_length=255, default="", null=True, blank=True)
	arrival_airport = models.CharField(max_length=255, default="", null=True, blank=True)
	departure_date = models.DateField(null=True, blank=True)
	departure_time = models.TimeField(null=True, blank=True)
	arrival_date = models.DateField(null=True, blank=True)
	arrival_time = models.TimeField(null=True, blank=True)
	check_in_status = models.CharField(max_length=255, default="Unverified", null=True, blank=True)
	check_luggage = models.CharField(max_length=255, default="Unverified", null=True, blank=True)
	forecast_provided = models.BooleanField(default=False, null=True, blank=True)
	trip_reason = models.CharField(max_length=255, default="", null=True, blank=True)
	time_stamp = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_delete = models.BooleanField(null=True, blank=True, default=False)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.ticket_number}"


class TripDetail(models.Model):
	"""
	Ticket trip detail model for storing the tickets trip data
	"""
	owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
	arrival_pickup_location = models.CharField(max_length=255, default="", null=True, blank=True)
	arrival_transfer_type = models.CharField(max_length=255, default="", null=True, blank=True)
	arrival_transfer_status = models.CharField(max_length=255, default="", null=True, blank=True)
	arrival_transfer_booked = models.CharField(max_length=255, default="", null=True, blank=True)
	arrival_transfer_eta = models.DateTimeField(null=True, blank=True)
	departure_dropoff_location = models.CharField(max_length=255, default="", null=True, blank=True)
	departure_transfer_type = models.CharField(max_length=255, default="", null=True, blank=True)
	departure_transfer_status = models.CharField(max_length=255, default="", null=True, blank=True)
	departure_transfer_booked = models.CharField(max_length=255, default="", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.owner.get_full_name()} - {self.ticket.ticket_number}"
	
	class Meta:
		ordering = ['-created_at']
