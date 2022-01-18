from rest_framework import generics
from SupportApp import serializer, models
from rest_framework.response import Response


# Create your views here.
class SupportTicketView(generics.ListCreateAPIView):
    serializer_class = serializer.SupportTicketSerializer
    queryset = models.TicketingForSupportModel.objects.all()


class SupportMessageView(generics.ListCreateAPIView):
    serializer_class = serializer.SupportMessageSerializer

    def get_queryset(self):
        ticketId = self.kwargs['ticketId']
        queryset = models.SupportMessageModel.objects.filter(ticket_id=ticketId)
        return queryset

    def perform_create(self, serializer):
        serializer.save(ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId']),
                        user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = serializer.data
        messaage = models.SupportMessageModel.objects.filter()
        for i in messaage:
            if i.user != self.request.user:
                i.is_read = True
                i.save()

        print(self.request.user)
        # if response['user'] != self.request.user:

        return Response(response)
