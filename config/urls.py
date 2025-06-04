from django.contrib import admin
from django.urls import path
from core.docs.views import DocumentAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/docs", DocumentAPIView.as_view(), name="document_api"),
]
