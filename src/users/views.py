from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, VerificationCode
from .serializers import (
    RequestRegisterSerializer, RegisterSerializer,
    ResetPasswordSerializer, ForgotPasswordSerializer,
    UserProfileRetrieveSerializer, UserProfileUpdateSerializer
)
from .services import UserServices
from .utils import (
    Util,
    INFO_RECOVERY_CODE_SENT,
    INFO_PASSWORD_RESET,
    AuthenticationException
)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except AuthenticationFailed:
            raise AuthenticationException()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestRegisterView(GenericAPIView):
    serializer_class = RequestRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_code = Util.generate_verification_code()
        VerificationCode.objects.create(email=email, code=verification_code)

        Util.send_mail(subject='Verification code', body=verification_code, to=[email])
        return Response(status=status.HTTP_200_OK)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def get_response_data(user):
        data = user.tokens
        data.update({'email': user.email})
        return Response(data, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        Util.validate_verification_code(
            email=serializer.validated_data['email'],
            verification_code=serializer.validated_data['verification_code']
        )
        instance = serializer.save()
        return self.get_response_data(instance)


class LogoutView(GenericAPIView):
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            verification_code = Util.generate_verification_code()
            VerificationCode.objects.create(email=email, code=verification_code)
            Util.send_mail('Recovery code', verification_code, to=[email])

        return Response(INFO_RECOVERY_CODE_SENT, status=status.HTTP_202_ACCEPTED)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_code = serializer.validated_data['code']
        raw_password = serializer.validated_data['password']

        Util.validate_verification_code(
            email=email,
            verification_code=verification_code
        )
        UserServices.reset_password(email, raw_password)

        return Response(INFO_PASSWORD_RESET, status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateAPIView):
    http_method_names = ['get', 'put']
    serializer_class = UserProfileUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            raise NotFound()
        serializer = UserProfileRetrieveSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            raise NotFound()

        instance = request.user.profile
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        result = UserProfileRetrieveSerializer(obj)
        return Response(result.data)
