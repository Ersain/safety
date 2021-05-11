from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, VerificationCode
from .serializers import (
    RequestRegisterSerializer, RegisterSerializer,
    ResetPasswordSerializer, ForgotPasswordSerializer
)
from .services import UserServices
from .utils import (
    Util,
    INFO_RECOVERY_CODE_SENT,
    INFO_PASSWORD_RESET,
    AuthenticationException
)


class LoginView(TokenObtainPairView):
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
    permission_classes = (IsAuthenticated,)

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
