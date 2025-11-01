# 🧳 ALX Travel App 0x02 — Chapa Payment Integration

A Django-based travel booking platform with integrated **Chapa API** for secure payment handling, supporting **payment initiation**, **verification**, and **status tracking**.

This project is a continuation of `alx_travel_app_0x01` and adds full payment functionality using the [Chapa Payment Gateway](https://developer.chapa.co/).

---

## 🚀 Features

- ✅ Secure Payment Integration with **Chapa**
- ✅ Booking with automatic **transaction reference generation**
- ✅ API endpoints for:
  - Payment initiation
  - Payment verification
- ✅ Payment status tracking: Pending / Completed / Failed
- ✅ Confirmation email sending (via Celery)
- ✅ Uses Chapa's **sandbox** for testing payments

---

## 📁 Project Structure

alx_travel_app_0x02/
├── listings/
│ ├── models.py # Payment model
│ ├── views.py # API views for payments
│ ├── urls.py # Endpoint routing
│ ├── tasks.py # Celery task for confirmation email
├── templates/
│ └── payment_success.html # Simple success page
├── .env # Store CHAPA_SECRET_KEY securely
├── README.md # You're here


---

## 🔐 Environment Variables

Create a `.env` file in the project root with:

```env
CHAPA_SECRET_KEY=your_chapa_test_secret_key

    Get this from your Chapa developer dashboard

    .

🔌 API Endpoints
🔁 Initiate Payment

URL: /api/initiate-payment/
Method: POST

Payload:

{
  "amount": "100",
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "0912345678"
}

Response:

{
  "checkout_url": "https://checkout.chapa.co/...",
  "booking_reference": "a57f7e8c-..."
}

✅ Verify Payment

URL: /api/verify-payment/?tx_ref=<tx_ref>
Method: GET

Response:

{
  "message": "Payment success"
}

💻 Payment Success Page

URL: /payment-success/?tx_ref=<tx_ref>
User is redirected here after completing payment on Chapa.
🧪 Testing Payments (Sandbox)

Use Chapa's sandbox with the following test card:

Card Number: 5399 8383 8383 8381
CVV: 470
Expiry: 10/30
PIN: 1234
OTP: 123456

Steps:

    Call /api/initiate-payment/

    Visit checkout_url

    Use the test card

    Complete payment

    Call /api/verify-payment/ to confirm and update status