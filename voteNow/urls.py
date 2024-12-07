from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Landing page
    path('connect/', views.next_page, name='connect'),  # Session creation and QR code display
    path('join/<uuid:session_key>/', views.join_session, name='join_session'),  # Join session by QR code
]
