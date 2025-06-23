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
    def post(self, requests):
        data = requests.data
        email = data.get('email')