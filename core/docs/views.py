import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.docs.models import Document
import requests

class DocumentAPIView(APIView):
    def post(self, request):
        content = request.data.get("content")
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = {
                "message": content
            }
            response = requests.post("http://127.0.0.1:8080/api/ai", json=data)
            if response.status_code != 200:
                return Response({"error": "Failed to process the request"}, status=response.status_code)
            return Response({"message": response}, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)