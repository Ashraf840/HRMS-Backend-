from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from . import models


# Custom JWT Authentication view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class RegisterView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserInfoListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.UserInfoModel.objects.all()


class UserAcdemicInfoListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserAcademicInfoSerializer

    def get_queryset(self):
        return models.UserAcademicInfoModel.objects.all()


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access')
        response.data = {
            'message': 'success'
        }
        return response
