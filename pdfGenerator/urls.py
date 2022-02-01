from django.urls import path
from .views import GeneratePDF
urlpatterns = [
    path('<applicationId>/', GeneratePDF.as_view())
]