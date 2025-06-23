import os
import tempfile
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.docs.models import Document
from django.core.mail import EmailMessage
from weasyprint import HTML
from django.template import Template, Context
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class PayAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        title: str  = request.data.get('title', "None")
        unit_price: float= request.data.get('unit_price')
        quantity: int = request.data.get("quantity")
        
        
        if not email  or not title or not unit_price or not quantity:
            return Response({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)