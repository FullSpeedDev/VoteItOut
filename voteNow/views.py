from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import Session
import qrcode
import base64
from io import BytesIO
import uuid

def index(request):
    return render(request, 'index.html')

def next_page(request):
    qr_code_img = None  # Base64-encoded QR code string
    session_id = None   # The session key for this instance

    if request.method == "POST":
        title = request.POST.get("title")  # Get session title from form
        session = Session.objects.create(title=title, session_key=uuid.uuid4())  # Create session

        # Generate session URL
        session_url = request.build_absolute_uri(f"/join/{session.session_key}/")

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(session_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert QR code image to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
        session_id = session.session_key  # Set session ID for use in the template

    return render(request, 'connect.html', {
        'qr_code_img': qr_code_img,
        'session_id': session_id,
    })



def join_session(request, session_key):
    session = get_object_or_404(Session, session_key=session_key)
    # Logic for handling user joining a session
    return render(request, 'session_detail.html', {'session': session})

# Utility function to generate QR codes
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to BytesIO
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), 'qr_code.png')
