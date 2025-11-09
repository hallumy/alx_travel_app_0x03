import requests
import uuid
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from django.http import HttpResponse
from .tasks import send_booking_confirmation_email


class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Listings to be viewed, created, updated, or deleted.

    - GET: List or retrieve Listings.
    - POST: Create a new Listing.
    - PUT/PATCH: Update an existing Listing.
    - DELETE: Remove a Listing.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Bookings to be viewed, created, updated, or deleted.

    - GET: List or retrieve Bookings.
    - POST: Create a new Booking.
    - PUT/PATCH: Update an existing Booking.
    - DELETE: Remove a Booking.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email
        send_booking_confirmation_email.delay(user_email, booking.id)

@api_view(['POST'])
def initiate_payment(request):
    amount = request.data.get("amount")
    email = request.data.get("email")
    booking_reference = str(uuid.uuid4())  # Generate a unique booking ref

    data = {
        "amount": amount,
        "currency": "ETB",
        "email": email,
        "first_name": request.data.get("first_name", "Customer"),
        "last_name": request.data.get("last_name", ""),
        "tx_ref": booking_reference,
        "callback_url": "http://localhost:8000/api/verify-payment/",  # Update for production
        "return_url": "http://localhost:8000/payment-success/",  # Page user sees after payment
        "customization[title]": "Travel Booking Payment"
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        Payment.objects.create(
            booking_reference=booking_reference,
            amount=amount,
            transaction_id=response_data['data']['tx_ref'],
            status='Pending'
        )
        return Response({
            "checkout_url": response_data['data']['checkout_url'],
            "booking_reference": booking_reference
        })
    else:
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")

    if not tx_ref:
        return Response({"error": "Transaction reference is required"}, status=400)

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    response = requests.get(verify_url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        status_from_chapa = result['data']['status']

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            payment.status = "Completed" if status_from_chapa == "success" else "Failed"
            payment.save()
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        return Response({"message": f"Payment {status_from_chapa}"})
    else:
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

def payment_success(request):
        return HttpResponse("Payment completed successfully.")
