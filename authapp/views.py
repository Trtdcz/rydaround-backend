from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import authenticate
from django.conf import settings
from authapp.models import MyUser, Ticket
from authapp.serializers import UserSerializer, TicketSerializer, UserDetailSerializer, TicketDetailSerializer, TicketListSerializer, TicketUpdateSerializer, DetailByCheckInStatusAndDepartureAirportSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication


class UserRegisterViewSet(viewsets.ModelViewSet):
	"""
	This view is used for registration
	"""
    
	serializer_class = UserSerializer
	permission_classes = (AllowAny,)

	def create(self, request, *args, **kwargs):	
		response: dict = dict()
		try:
			password: str = request.data.get('password')
			confirm_password: str = request.data.get('confirm_password')
			serializer_data = UserSerializer(data=request.data)
			if serializer_data.is_valid():
				if confirm_password:
					if len(confirm_password) >= 10:
						if password == confirm_password:
							serializer_data.save()
							data = {key: value for key, value in serializer_data.data.items() if key != "password"}
							response['status'] = True
							response['data'] = data
						else:
							response['status'] = False
							response['error'] = 'Password and Confirm Password not matched'	
					else:
						response['status'] = False
						response['error'] = {'confirm_password': 'Confirm_password length should be equal or greater then 10 character.'}
				else:
					response['status'] = False
					response['error'] = {'confirm_password': 'This field may not be blank.'}
			else:
				response['status'] = False
				response['error'] = serializer_data.errors
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)


class LogoutAPIView(APIView):
	"""
	This view is used for logout"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def post(self, request):
		response: dict = dict()
		try:
			request.user.auth_token.delete()
			logout(request)
			response['status'] = True
			response['data'] = list()	
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)


class TicketsAPIView(APIView):
	"""
	This view is used for get the all tickets list and create the ticket.
	"""

	def get(self, request):
		response: dict = dict()
		try:
			all_tickets = Ticket.objects.filter(is_delete=False).order_by('created_at')
			serializer_data = TicketListSerializer(all_tickets, many=True)
			response['status_code'] = status.HTTP_200_OK
			response['data'] = serializer_data.data
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)

	def post(self, request):
		response: dict = dict()
		try:
			serializer_data = TicketSerializer(data=request.data)
			if serializer_data.is_valid():
				serializer_data.save()
				response['status'] = True
				response['data'] = serializer_data.data
			else:
				response['status'] = False
				response['error'] = serializer_data.errors
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)
	
	def put(self, request, pk):
		response: dict = dict()
		try:
			if Ticket.objects.filter(pk=pk, is_delete=False).exists():
				ticket_object = Ticket.objects.get(pk=pk, is_delete=False)
				serializer_data = TicketUpdateSerializer(ticket_object, data=request.data)
				if serializer_data.is_valid():
					serializer_data.save()
					response['status'] = True
					response['data'] = serializer_data.data
				else:
					response['status'] = False
					response['error'] = serializer_data.errors
			else:
				response['status'] = False
				response['error'] = "Ticket doesn't exists."
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)

	def delete(self, request, pk):
		response: dict = dict()
		try:
			if Ticket.objects.filter(pk=pk, is_delete=False).exists():
				ticket_object = Ticket.objects.get(pk=pk, is_delete=False)
				ticket_object.is_delete = True
				ticket_object.save()
				response['status'] = True
				response['data'] = []
			else:
				response['status'] = False
				response['error'] = "Ticket doesn't exists."
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)


class UserTicketListAPIView(APIView):
	def get(self, request, pk):
		response: dict = dict()
		try:
			if MyUser.objects.filter(pk=pk, is_active=True).exists() is True:
				user_object = MyUser.objects.get(pk=pk, is_active=True)
				user_tickets_data = Ticket.objects.filter(owner=user_object, is_delete=False).order_by('-created_at')
				serializer_data = UserDetailSerializer(user_object, context={'ticket_data': user_tickets_data})
				response['status'] = True
				response['data'] = serializer_data.data
			else:
				response['status'] = False
				response['error'] = "User doesn't exists."	
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)


class TicketDetailAPIView(APIView):
	def get(self, request, pk):
		response: dict = dict()
		try:
			if Ticket.objects.filter(pk=pk, is_delete=False).exists():
				ticket_object = Ticket.objects.get(pk=pk, is_delete=False)
				serializer_data = TicketListSerializer(ticket_object)
				response['status'] = True
				response['data'] = serializer_data.data
			else:
				response['status'] = False
				response['error'] = "Ticket doesn't exists."
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)


class GetUserAndFlightInfoByDepartureAirportAndCheckInStatusView(APIView):
	def get(self, request, departure_airport, check_in_status):
		response: dict = dict()
		try:
			
			ticket_object = Ticket.objects.filter(departure_airport__icontains=departure_airport, check_in_status__icontains=check_in_status, is_delete=False)
			serializer_data = DetailByCheckInStatusAndDepartureAirportSerializer(ticket_object, many=True)
			response['status'] = True
			response['data'] = serializer_data.data
		except Exception as e:
			response['status'] = False
			response['error'] = str(e)
		return Response(response)
