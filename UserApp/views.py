"""
Problem may occur just because of serializer name
it may conflict
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics, status, views, response
from . import serializer
from . import models
from .permissions import IsOwner,IsSuperUser


# Custom JWT Authentication view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


# User Registration view inheriting APIView class
class RegisterView(views.APIView):
    # permission_classes = [permission.IsAuthenticated]

    def post(self, request):
        serializers = serializer.UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return response.Response(serializers.data)


# User info View
# Retrieving data from User model data
class UserInfoListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserSerializer

    def get_queryset(self):
        return models.UserInfoModel.objects.all()


# User academic information View
# if user is authenticate user can Retrieve data
class UserAcademicInfoListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserAcademicSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        u_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id)


class UserAcademicInfoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserAcademicSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        u_id = self.kwargs['uid']
        a_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id, id=a_id)


class LogoutView(views.APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return response.Response(status=status.HTTP_200_OK)


# Retrieving Data From Multiple model -
# Model name:
# User,
# UserAcademicInfoModel,
# UserCertificationsModel,
# UserTrainingExperienceModel
# =================================

# class UserInfoApiView(ObjectMultipleModelAPIView):
#     def get_querylist(self):
#         id = self.kwargs['id']
#         print(id)
#         # current_user = models.User.objects.get(id=id)
#
#         # print(current_user)
#         querylist = (
#             # {'queryset': models.User.objects.all(),
#             #  'serializer_class': serializers.UserInfoSerializer},
#             {'queryset': models.UserAcademicInfoModel.objects.all(),
#              'serializer_class': serializers.UserAcademicSerializer},
#         )
#
#         return querylist


# specific User information retrieve
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserDetailsSerializer
    queryset = models.User.objects.all()
    lookup_field = 'id'

#
class UpdateAcademicInfoView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = serializer.UpdateAcademicInformationSerializer
    queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        u_id = self.kwargs['id']

        # a_id = self.kwargs['id']

        return models.UserAcademicInfoModel.objects.filter(user_id=u_id)
