from django.shortcuts import render
from .models import User
from .serializer import RegisterSerializer, UserSerializerAdmin, UserSerializerNormal
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView

from rest_framework import decorators, permissions as rest_permission
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken

from django.middleware import csrf
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework.pagination import PageNumberPagination


# ---------------generating-token----------

class CustumPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return ({
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    })

# -------------------register-api-----------


@decorators.permission_classes([rest_permission.AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_verification()
            self.send_email(user)
            user.save()
            return Response({
                "message": "User Registered Successfully and a verification otp is send to user's email",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }
            )

    def send_email(self, user):
        otp = user.generate_verification()
        verification = reverse('verify', args=[otp])
        main_otp = verification.split('/')[-2]

        subject = "Registration Verification OTP"
        message = (f"Hi {user.first_name} {user.last_name}\n"
                   f"This is User Veridfication OTP: {main_otp}\n"
                   f"If you did not make this request, please ignore this email.")

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


# -------------------------verifying-the-user------------------------
@decorators.permission_classes([rest_permission.AllowAny])
class VerifyView(APIView):

    def get(self, request, otp):
        user = self.get_user(otp)

        if user:
            user.is_active = True
            user.verification_code = None
            self.send_email(user)
            user.save()
            return Response({
                "message": "User Verified Successfully",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "Invalid OTP",
                "status": status.HTTP_400_BAD_REQUEST
            })

    def get_user(self, otp):
        try:
            user = User.objects.get(verification_code=otp, is_active=False)
            return user
        except:
            return None

    def send_email(self, user):
        subject = "Registration Verification Confermation"
        message = (f"Hi {user.first_name} {user.last_name}"
                   f"You are successfully verified.\n"
                   f"Now you can use our web aplication to its full extent.")

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


# -----------------resend-verification-otp-------------------------
@decorators.permission_classes([rest_permission.AllowAny])
class ResendVerificationCOdeView(APIView):
    def post(self, request):
        email = request.data.get('email')

        user = User.objects.get(email=email, is_active=False)

        if user:
            user.generate_verification()
            self.send_email(user)
            user.save()
            return Response({
                "message": "New Verification code resent successfully",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "Invalid email address.",
                "status": status.HTTP_400_BAD_REQUEST
            })

    def send_email(self, user):
        otp = user.generate_verification()
        verification = reverse('verify', args=[otp])
        main_otp = verification.split('/')[-2]
        subject = "NEw Verificationn code send"
        message = (f"hi {user.first_name} {user.last_name}\n"
                   f"this is your new verification code: {main_otp}\n")
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


# --------------------------login-api------------------------------
@decorators.permission_classes([rest_permission.AllowAny])
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({
                "message": "Invalid Username",
                "status": status.HTTP_200_OK
            })

        if not user.check_password(password):
            return Response({
                "message": "Incorrect Password",
                "status": status.HTTP_400_BAD_REQUEST
            })

        response = Response()

        token = generate_token(user)

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token['access_token'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=token['refresh_token'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )

        response.data = {
            "message": "login successful",
            "status": status.HTTP_200_OK,
            "access_token": token['access_token'],
            "refresh_token": token['refresh_token']
        }
        response['CSRFToken'] = csrf.get_token(request)
        return response

# -----------------------------------user-profile----------------------------


@decorators.permission_classes([rest_permission.IsAuthenticated])
class UserProfileView(APIView):
    def get(self, request):
        user = request.user

        serializer = UserSerializerAdmin(user, many=False)
        return Response({
            "message": "user profile",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })
# -----------------------update-user-----------------------


@decorators.permission_classes([rest_permission.IsAuthenticated])
class UpdateUserProfile(APIView):
    def patch(self, request, id=None):
        user = User.objects.get(id=id)
        if user.username == self.request.user.username:
            serializer = UserSerializerNormal(
                user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "User Data Updated Successfully",
                    "status": status.HTTP_200_OK
                })
            return Response({
                "message": "User Not Updated",
                "status": status.HTTP_400_BAD_REQUEST
            })
        else:
            return Response({
                "message": "Unauthorized",
                "status": status.HTTP_200_OK
            })

# --------------------------logout -----------------------


@decorators.permission_classes([rest_permission.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        )
        token = tokens.RefreshToken(refresh_token)
        token.blacklist()
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response.delete_cookie('X-CSRFToken')
        response.delete_cookie('csrftoken')

        response.data = {
            "message": "user logout successful",
            "status": status.HTTP_200_OK
        }
        return response


# -----------------------forgot-password--------------------------------
@decorators.permission_classes([rest_permission.AllowAny])
class ForgotPasswordEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')

        user = User.objects.get(email=email)

        if user:
            user.generate_forgot()
            self.send_email(user)
            user.save()
            return Response({
                "message": "Forgot password confermation code sent successfully to registered Email",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "Invalid email address.",
                "status": status.HTTP_400_BAD_REQUEST
            })

    def send_email(self, user):
        code = user.generate_forgot()
        verification = reverse('forgot', args=[code])
        main_code = verification.split('/')[-2]
        subject = "Forgot password confirmation code"
        message = (f"hi {user.first_name}{user.last_name},\n"
                   f"This is your forgot password confermation code: {
                       main_code}."
                   f"Thank you.")
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@decorators.permission_classes([rest_permission.AllowAny])
class ForgotPasswordVerifyView(APIView):
    def get(self, request, otp):
        user = self.get_user(otp)
        if user:
            user.forgot = None
            user.is_forgot = True
            user.save()
            return Response({
                "message": "Forgot password confirmation code verified successfully",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "Invalid OTP",
                "status": status.HTTP_400_BAD_REQUEST
            })

    def get_user(self, otp):
        try:
            user = User.objects.get(forgot=otp, is_forgot=False)
            return user
        except User.DoesNotExist:
            return None


@decorators.permission_classes([rest_permission.AllowAny])
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        conf_password = request.data.get('conf_password')

        user = User.objects.get(email=email, is_forgot=True)

        if user is None:
            return None

        if password != conf_password:
            return Response({
                "message": "Passwords do not match",
                "status": status.HTTP_400_BAD_REQUEST
            })

        user.set_password(password)
        user.is_forgot = False
        user.save()
        self.send_email(user)
        return Response({
            "message": "Password reset successfully",
            "status": status.HTTP_200_OK
        })

    def send_email(self, user):
        subject = "Password Change Successfully"
        message = (f"Hi {user.first_name} {user.last_name},\n"
                   f"Your Password have changes successfully\n")

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@decorators.permission_classes([rest_permission.AllowAny])
class ResendResetPasswordVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email, is_forgot=False)
        if user:
            user.generate_forgot()
            self.send_email(user)
            user.save()
            return Response({
                "message": "New Forgot password confermation code sent successfully",
                "status": status.HTTP_200_OK
            })

    def send_email(self, user):
        code = user.generate_forgot()
        verification = reverse('forgot', args=[code])
        main_code = verification.split('/')[-2]
        subject = "New Forgot password confirmation code"
        message = (f"hi {user.first_name}{user.last_name},\n"
                   f"This is your New forgot password confermation code: {
                       main_code}."
                   f"Thank you.")
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

# -----------------------------------------------Admin---------------------------------------------------------------


@decorators.permission_classes([rest_permission.IsAdminUser])
class UserListView(APIView):
    pagination_class = CustumPagination

    def get(self, request):
        users = User.objects.all()
        pagination = self.pagination_class()
        result = pagination.paginate_queryset(users, request)
        serializer = UserSerializerAdmin(result, many=True)
        return Response({
            "message": "user list",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })


@decorators.permission_classes([rest_permission.IsAdminUser])
class EditUserView(APIView):
    def patch(self, request, id=None):
        user = User.objects.get(id=id)
        serializer = UserSerializerAdmin(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "user updated successfully",
                "status": status.HTTP_200_OK
            })
        return Response({
            "message": "user not updated",
            "status": status.HTTP_400_BAD_REQUEST
        })


@decorators.permission_classes([rest_permission.IsAdminUser])
class DeleteUserView(APIView):
    def delete(self, request, id=None):
        user = User.objects.get(id=id)
        user.delete()
        return Response({
            "message": "user deleted successfully",
            "status": status.HTTP_200_OK
        })
