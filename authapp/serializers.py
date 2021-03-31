from rest_framework import serializers
from authapp.models import MyUser, Ticket, TripDetail
from django.core.validators import MinLengthValidator
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(required=True)
	last_name = serializers.CharField(required=True)
	middle_name = serializers.CharField(required=True)
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=MyUser.objects.all())])
	password = serializers.CharField(required=True, validators=[MinLengthValidator(10)])
	username = serializers.CharField(read_only=True)
	user_id = serializers.SerializerMethodField()

	class Meta:
		model  = MyUser
		fields =  (
			'user_id', 'first_name', 'last_name', 'middle_name', 
			'email', 'username', 'password', 'phone_number',
		)

	def get_user_id(self, obj):
		return obj.pk
		
	def create(self, validated_data):
		validated_data.update({'username': validated_data.get('email')})
		user = MyUser.objects.create_user(**validated_data)
		user.set_password(validated_data.get('password'))
		user.save()
		return user


class TripDetailSerializer(serializers.ModelSerializer):
	arrival_pickup_location = serializers.CharField(required=True)
	arrival_transfer_type = serializers.CharField(required=True)
	arrival_transfer_status = serializers.CharField(required=True)
	arrival_transfer_booked = serializers.CharField(required=True)
	arrival_transfer_eta = serializers.DateTimeField(required=True)
	departure_dropoff_location = serializers.CharField(required=True)
	departure_transfer_type = serializers.CharField(required=True)
	departure_transfer_status = serializers.CharField(required=True)
	departure_transfer_booked = serializers.CharField(required=True)
	
	class Meta:
		model = TripDetail
		fields = (
			'arrival_pickup_location', 'arrival_transfer_type', 'arrival_transfer_status',
			'arrival_transfer_booked', 'arrival_transfer_eta', 'departure_dropoff_location',
			'departure_transfer_type', 'departure_transfer_status', 'departure_transfer_booked',
		)


class TicketListSerializer(serializers.ModelSerializer):
	ticket_id = serializers.SerializerMethodField()
	trip_detail = serializers.SerializerMethodField()

	class Meta:
		model = Ticket
		fields = (
			'ticket_id', 'owner', 'ticket_number', 'airline_name', 'airline_iata_code', 'airline_icao_code',
			'flight_number', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time',
			'arrival_date', 'arrival_time', 'check_in_status', 'time_stamp', 'trip_detail',
		)

	def get_ticket_id(self, obj):
		return obj.pk
	
	def get_trip_detail(self, obj):
		trip_object = TripDetail.objects.get(owner=obj.owner, ticket=obj)
		serializer_data = TripDetailSerializer(trip_object)
		return serializer_data.data


class TicketSerializer(serializers.ModelSerializer):
	owner_id = serializers.IntegerField(required=True)
	ticket_number = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Ticket.objects.all())])
	airline_name = serializers.CharField(required=True)
	airline_iata_code = serializers.CharField(required=True)
	airline_icao_code = serializers.CharField(required=True)
	flight_number = serializers.CharField(required=True)
	departure_airport = serializers.CharField(required=True)
	arrival_airport = serializers.CharField(required=True)
	departure_date = serializers.DateField(required=True)
	departure_time = serializers.TimeField(required=True)
	arrival_date = serializers.DateField(required=True)
	arrival_time = serializers.TimeField(required=True)
	check_in_status = serializers.CharField(required=True)
	check_luggage = serializers.CharField(required=True)
	forecast_provided = serializers.BooleanField(required=True)
	trip_reason = serializers.CharField(required=True)
	time_stamp = serializers.DateTimeField(required=True)
	trip_detail = TripDetailSerializer(required=True)

	class Meta:
		model = Ticket
		fields = (
			'owner_id', 'ticket_number', 'airline_name', 'airline_iata_code', 'airline_icao_code',
			'flight_number', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time',
			'arrival_date', 'arrival_time', 'check_in_status', 'check_luggage', 'forecast_provided',
			'trip_reason', 'time_stamp', 'trip_detail',
			)
	
	def validate_owner_id(self, pk):
		if MyUser.objects.filter(pk=pk, is_active=True).exists() is False:
			raise serializers.ValidationError('Owner ID not exists.')
		else:
			return pk

	def create(self, validated_data):
		ticket_object = Ticket.objects.create(
			owner_id=validated_data.get('owner_id'), ticket_number=validated_data.get('ticket_number'), airline_name=validated_data.get('airline_name'),
			airline_iata_code=validated_data.get('airline_iata_code'), airline_icao_code=validated_data.get('airline_icao_code'), flight_number=validated_data.get('flight_number'), departure_airport=validated_data.get('departure_airport'), arrival_airport=validated_data.get('arrival_airport'),
			departure_date=validated_data.get('departure_date'), departure_time=validated_data.get('departure_time'), arrival_date=validated_data.get('arrival_date'), arrival_time=validated_data.get('arrival_time'), check_in_status=validated_data.get('check_in_status'),
			check_luggage=validated_data.get('check_luggage'), forecast_provided=validated_data.get('forecast_provided'), trip_reason=validated_data.get('trip_reason'), time_stamp=validated_data.get('time_stamp')
		)
		trip_detail_data = validated_data.get('trip_detail')
		trip_detail_data.update({'owner': ticket_object.owner, 'ticket': ticket_object})
		TripDetailSerializer.create(TripDetailSerializer(), validated_data=trip_detail_data)
		return validated_data


class TicketDetailSerializer(serializers.ModelSerializer):
	ticket_id = serializers.SerializerMethodField()

	class Meta:
		model = Ticket
		fields = (
			'ticket_id', 'ticket_number', 'flight_number', 'departure_airport',
			'arrival_airport', 'departure_date', 'departure_time',
			'arrival_date', 'arrival_time',
		)

	def get_ticket_id(self, obj):
		return obj.id


class UserDetailSerializer(serializers.ModelSerializer):
	tickets = serializers.SerializerMethodField()
	user_id = serializers.SerializerMethodField()

	class Meta:
		model = MyUser
		fields = ('user_id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'tickets')

	def get_tickets(self, obj):
		tickets_object = self.context.get('ticket_data')
		serializer_data = TicketDetailSerializer(tickets_object, many=True)
		return serializer_data.data

	def get_user_id(self, obj):
		return obj.pk


class TicketUpdateSerializer(serializers.ModelSerializer):
	airline_name = serializers.CharField(required=True)
	airline_iata_code = serializers.CharField(required=True)
	airline_icao_code = serializers.CharField(required=True)
	flight_number = serializers.CharField(required=True)
	departure_airport = serializers.CharField(required=True)
	arrival_airport = serializers.CharField(required=True)
	departure_date = serializers.DateField(required=True)
	departure_time = serializers.TimeField(required=True)
	arrival_date = serializers.DateField(required=True)
	arrival_time = serializers.TimeField(required=True)
	check_in_status = serializers.CharField(required=True)
	check_luggage = serializers.CharField(required=True)
	forecast_provided = serializers.BooleanField(required=True)
	trip_reason = serializers.CharField(required=True)
	time_stamp = serializers.DateTimeField(required=True)
	trip_detail = TripDetailSerializer(required=True)

	class Meta:
		model = Ticket
		fields = (
			'owner_id', 'ticket_number', 'airline_name', 'airline_iata_code', 'airline_icao_code',
			'flight_number', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time',
			'arrival_date', 'arrival_time', 'check_in_status', 'check_luggage', 'forecast_provided',
			'trip_reason', 'time_stamp', 'trip_detail',
			)


class DetailByCheckInStatusAndDepartureAirportSerializer(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	middle_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	
	class Meta:
		model = Ticket
		fields = ('first_name', 'middle_name', 'last_name', 'flight_number', 'departure_time')
	
	def get_first_name(self, obj):
		return obj.owner.first_name
	
	def get_middle_name(self, obj):
		return obj.owner.middle_name

	def get_last_name(self, obj):
		return obj.owner.last_name
