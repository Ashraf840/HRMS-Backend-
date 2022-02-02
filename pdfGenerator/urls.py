from django.urls import path
from .views import GeneratePDF, ViewAppointMentLetterView
# urlpatterns = [
#     path('<applicationId>/', GeneratePDF.as_view()),
#     path('view/<applicationId>/', ViewAppointMentLetterView.as_view())
# ]