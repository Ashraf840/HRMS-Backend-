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
        # print(applicationId)
        checkRedundant = OfficialDocumentsModel.objects.filter(applicationId=applicationId)
        # print(checkRedundant)
        if len(checkRedundant) > 0:
            data = checkRedundant.get()
            return Response({'detail': 'Already created', 'appointment_letter': data.appointmentLetter})
        userInfo = UserJobAppliedModel.objects.get(id=applicationId)
        prams = {
            'today': datetime.date.today(),
            'user_info': userInfo
        }
        file_name, status = save_pdf(prams)

        if not status:
            return Response({'detail': 'pdf generate failed'})
        else:
            OfficialDocumentsModel.objects.create(applicationId=userInfo,
                                                  appointmentLetter=f'/media/OfficialDocuments/{file_name}.pdf')
            return Response({
                'status': 200,
                'path': f'/media/OfficialDocuments/{file_name}.pdf'
            })
