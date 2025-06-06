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


class DocumentAPIView(APIView):
    def post(self, request):
        content = request.data.get("content")
        send_to = request.data.get("send_to")

        if not content or not send_to:
            return Response(
                {"error": "Os campos 'content' e 'send_to' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.post("http://127.0.0.1:8080/api/ai", json={"message": content})
            response.raise_for_status()

            response_data = response.json()
            ai_response = response_data.get("response")
            if not ai_response:
                return Response(
                    {"error": "Resposta inválida do serviço de IA."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            new_document = Document.objects.create(
                title=ai_response.get("title", "Sem título"),
                content=ai_response.get("summary", ""),
                send_to=send_to,
            )

            html_template = """
            <html>
            <head>
                <meta charset="utf-8">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #2c3e50; }
                    p { font-size: 16px; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <p>{{ content }}</p>
            </body>
            </html>
            """
            template = Template(html_template)
            context = Context({"title": new_document.title, "content": new_document.content})
            html_content = template.render(context)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                HTML(string=html_content).write_pdf(pdf_file.name)
                pdf_path = pdf_file.name

            email = EmailMessage(
                subject=f"Documento: {new_document.title}",
                body="Segue em anexo o PDF gerado a partir do seu conteúdo.",
                from_email="martinsbarroskaua@gmail.com",
                to=[send_to],
            )
            email.attach_file(pdf_path)
            email.send()

            os.unlink(pdf_path)

            return Response(
                {
                    "message": "Documento criado e enviado por email com sucesso!",
                    "uuid": new_document.uuid,
                    "title": new_document.title,
                    "content": new_document.content,
                },
                status=status.HTTP_201_CREATED,
            )

        except requests.RequestException as e:
            return Response({"error": f"Erro ao comunicar com o serviço de IA: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
