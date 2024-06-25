from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from .models import User
from .serializers import(
    UserSerializer,
    UserLoginSerializer
)



class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
class UserLoginViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # If user is authenticated, generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        

class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]