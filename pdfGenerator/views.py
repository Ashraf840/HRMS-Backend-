import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from UserApp.models import User
from .pdf_helper import save_pdf
from RecruitmentManagementApp.models import UserJobAppliedModel, OfficialDocumentsModel


# Create your views here.


class GeneratePDF(APIView):
    def get(self, request, applicationId):
        try:
            checkRedundant = OfficialDocumentsModel.objects.filter(applicationId_id=applicationId)
            if checkRedundant is not None:
                return Response({'detail': 'Already created'})
        except:
            userInfo = UserJobAppliedModel.objects.filter(applicationId_id=applicationId)
            prams = {
                'today': datetime.date.today(),
                'user_info': userInfo
            }
            file_name, status = save_pdf(prams)

            if not status:
                return Response({'detail': 'pdf generate failed'})
            else:

                return Response({
                    'status': 200,
                    'path': f'/media/OfficialDocuments/{file_name}.pdf'
                })





