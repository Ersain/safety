from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from files.services.s3 import S3Services
from .models import User, UserProfile, GenderChoices
from .services import UserServices
from .utils import IgnoreCaseChoiceField


class RequestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class RegisterSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField()
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=3, write_only=True)

    class Meta:
        fields = ('verification_code', 'email', 'password', 'password_confirm')
        model = User

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Passwords didn't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('verification_code')
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6)
    password_confirm = serializers.CharField(min_length=6)
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Passwords didn't match")
        return attrs


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    gender = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('photo', 'phone_number', 'username', 'gender', 'email')

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_photo(self, obj):
        if obj.photo:
            return S3Services.generate_object_url(obj.photo.name)
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    gender = IgnoreCaseChoiceField(GenderChoices.choices)

    class Meta:
        model = UserProfile
        fields = ('photo', 'phone_number', 'username', 'gender', 'email')

    def update(self, instance, validated_data):
        UserServices.update_email_field(
            user=self.context['request'].user,
            email=validated_data.pop('email', '')
        )
        return super().update(instance, validated_data)
