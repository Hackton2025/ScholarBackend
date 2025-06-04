from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.docs.models import Document
import requests

class DocumentAPIView(APIView):
    def post(self, request):
        content  = request.data.get('content')
        title = request.data.get('title')
        send_to = request.data.get('send_to')
        
        if not content or not title or not send_to:
            return Response({"message": "Content, title and teacher email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            json = {
                "message": content
            }
            response = requests.post("http://localhost:8000/api/ai", json=json )
            print(response)
            if not response:
                return Response({"message": "AI service is not available"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            data = response.json()
            return Response({"message": data}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)