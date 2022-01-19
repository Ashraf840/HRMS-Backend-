from rest_framework import generics, status, permissions
from SupportApp import serializer, models
from rest_framework.response import Response


# Create your views here.
class SupportTicketView(generics.ListCreateAPIView):
    serializer_class = serializer.SupportTicketSerializer
    queryset = models.TicketingForSupportModel.objects.all()


class SupportMessageView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.SupportMessageSerializer

    def get_queryset(self):
        ticketId = self.kwargs['ticketId']
        queryset = models.SupportMessageModel.objects.filter(ticket_id=ticketId)
        return queryset

    def perform_create(self, serializer):
        serializer.save(ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId']),
                        user=self.request.user)

    def create(self, request, *args, **kwargs):
        ticket = models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId'])
        if self.request.user.is_employee or (self.request.user == ticket.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You are not employee or author'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        ticket = models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId'])
        if self.request.user.is_employee or (self.request.user == ticket.user):
            serializer = self.get_serializer(self.get_queryset(), many=True)
            response = serializer.data
            messaage = models.SupportMessageModel.objects.filter()
            for i in messaage:
                if i.user != self.request.user:
                    i.is_read = True
                    i.save()
            return Response(response)
        return Response({'detail': 'You are not employee or author'}, status=status.HTTP_400_BAD_REQUEST)
