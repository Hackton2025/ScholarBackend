import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.docs.models import Document
import requests

class DocumentAPIView(APIView):
    def post(self, request):
        content = request.data.get("content")
        send_to = request.data.get("send_to")
        
        if not content or not send_to:
            return Response({"error": "Content and send_to are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = {
                "message": content,
                "model": "command-r"  
            }
            response = requests.post("http://127.0.0.1:8080/api/ai", json=data)
            
            if response.status_code != 200:
                return Response({"error": "Failed to process the request"}, status=response.status_code)

            response_data = response.json()
            ai_response = response_data.get("response")

            if not ai_response:
                return Response({"error": "Invalid response from AI service"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            new_document = Document.objects.create(
                title=ai_response.get("title"),
                content=ai_response.get("summary"),
                send_to=send_to
            )

            return Response({"message": "New document created successfully!", "uuid": new_document.uuid, "message": new_document.content,  "title": new_document.title}, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
