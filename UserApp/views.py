"""
Problem may occur just because of serializer name
it may conflict
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics, status, views, response
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializer
from . import models


# Custom JWT Authentication view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


# JWT logout
# class LogoutView(generics.DestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     print('upper')
#     def post(self, request):
#         print('called')
#         try:
#             refresh_token = request.data["refresh_token"]
#             print(refresh_token)
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return response.Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return response.Response(status=status.HTTP_400_BAD_REQUEST)


# User Registration view inheriting APIView class
class RegisterView(generics.CreateAPIView):
    serializer_class = serializer.UserRegistrationSerializer
    queryset = models.User.objects.all()
    # permission_classes = [permission.IsAuthenticated]

    # def post(self, request):
    #     serializers = serializer.UserInfoSerializer(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializers.save()
    #     return response.Response(serializers.data)


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


# Updating Academic information
# academicInformation update view
class AddAcademicInfoView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializer.UserAcademicSerializer
    queryset = models.UserAcademicInfoModel.objects.all()


# Academic Information Update Retrieve & Update View
class UpdateAcademicInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UpdateAcademicInformationSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        u_id = self.kwargs['user__id']

        return models.UserAcademicInfoModel.objects.filter(user__id=u_id, id=id)


# Work Experience CRUD Operations
class AddWorkExperienceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    queryset = models.UserWorkingExperienceModel.objects.all()


class UpdateWorkExpInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        w_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserWorkingExperienceModel.objects.filter(user__id=u_id, id=w_id)


# Certification CRUD operations

class AddCertificationsView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserCertificationsSerializer
    queryset = models.UserCertificationsModel.objects.all()


class UpdateCertificationsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserCertificationsSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserCertificationsModel.objects.filter(user__id=u_id, id=c_id)


# Training CRUD operations

class AddTrainingExperienceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    queryset = models.UserTrainingExperienceModel.objects.all()


class UpdateTrainingExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserTrainingExperienceModel.objects.filter(user__id=u_id, id=c_id)
