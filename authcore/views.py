import random
from django.db.models import Q 
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, logout


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from fcm_django.models import FCMDevice

from .permissions import IsVerifiedUser
from utils.token_generator import get_or_create_token
from utils.otp_handler import send_otp
from . import serializers, models


from rest_framework.decorators import api_view, permission_classes, authentication_classes

User = get_user_model()

# Create your views here.
class UserRegisterView(generics.GenericAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                user = models.User.objects.get(phone_number=serializer.data['phone_number'])
                
                # send otp
                generated_otp = random.randint(1000, 9999)
                models.Otp.objects.create(user=user, otp=generated_otp)
                
                send_otp.delay(
                    phone_number=str(serializer.data['phone_number']), otp=generated_otp 
                )
                
                # create token but not sending in response
                token = get_or_create_token(user)

                return Response({
                    'message': 'User Created Successfully! Please verify your phone number.',
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data, context={'request': request})
            if serializer.is_valid():
                
                email_or_phone_number = serializer.validated_data['email_or_phone_number']
                password = serializer.validated_data['password']
                fcm_token = serializer.validated_data['fcm_token']
                device_type = serializer.validated_data['device_type']

                user = authenticate(email_or_phone=email_or_phone_number, password=password)
                if user is not None:
                    if user.verified is True:
                        token = get_or_create_token(user)
                        fcm_obj = FCMDevice.objects.filter(registration_id=fcm_token).first()
                        if fcm_obj is not None:
                            fcm_obj.delete()

                        # register device
                        FCMDevice.objects.create(
                            user=user,
                            name=user.full_name.split(' ')[0] + "'s Device",
                            registration_id=fcm_token,
                            type=device_type,
                            active=True
                        )
                        return Response({
                            'id' : user.id,
                            'message': 'User Logged In Successfully!',
                            'token': token.key
                        }, status=status.HTTP_200_OK)                    
                    return Response({
                        'error': 'Please verify your phone number!'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                return Response({
                    'error': 'Invalid Credentials!'
                }, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OtpVerifyView(generics.GenericAPIView):
    serializer_class = serializers.OtpVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                user = models.User.objects.get(phone_number=serializer.validated_data['phone_number'])

                otp = serializer.validated_data['otp']
                if user is not None:
                    otp_obj = models.Otp.objects.filter(user=user, otp=otp).first()
                    if otp_obj is None:
                        return Response({
                            'error': 'Invalid OTP'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    # update user
                    user.verified = True
                    user.save()
                    
                    token = get_or_create_token(user)

                    # update otp
                    otp_obj.has_used = True
                    otp_obj.save()

                    return Response({
                        'message': 'OTP Verified Successfully',
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'User Not Found '
                }, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ProfilePictureView(generics.GenericAPIView):
    serializer_class = serializers.ProfilePictureSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                user = request.user
                user.profile_picture = serializer.validated_data['profile_picture']
                user.save()
                return Response({
                    'message': 'Profile Picture Uploaded Successfully!'
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request):
        try:
            user = request.user
            return Response({
                'profile_picture': user.profile_picture.url
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgotPasswordOtpRequestView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordOtpRequestSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                phone_number = serializer.validated_data['phone_number']
                user = models.User.objects.filter(phone_number=phone_number).first()
                if user is not None:
                    user.verified = False
                    user.save()
                    
                    generated_otp = random.randint(1000, 9999)
                    models.Otp.objects.create(user=user, otp=generated_otp, has_used=False)
                    
                    # send the otp
                    send_otp.delay(
                        phone_number=str(serializer.data['phone_number']), otp=generated_otp 
                    )
                    
                    return Response({
                        'message': 'OTP sent successfully! Please verify your phone number.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'User with this Phone Number Not Found!'
                }, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgotPasswordOtpVerifyView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordOtpVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                phone_number = serializer.validated_data['phone_number']
                otp = serializer.validated_data['otp']
                user = models.User.objects.filter(phone_number=phone_number).first()
                if user is not None:
                    otp_obj = models.Otp.objects.filter(user=user, otp=otp).first()
                    if otp_obj is None:
                        return Response({
                            'error': 'Invalid OTP'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    otp_obj.has_used = True
                    otp_obj.save()
                    user.verified = True
                    user.save()
                    return Response({
                        'message': 'OTP Verified Successfully!'
                    }, status=status.HTTP_200_OK)
                return Response({
                    "error": "User with this Phone Number Not Found!"
                }, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['new_password']
            user = models.User.objects.filter(phone_number=phone_number).first()
            if user is not None:
                user.set_password(password)
                user.save()
                return Response({
                    'message': 'Password Changed Successfully!'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'User with this Phone Number Not Found!'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    try:
        user = request.user
        fcm_obj = FCMDevice.objects.filter(user=user)
        for device in fcm_obj:
            device.delete()
        logout(request)
        return Response({
            'message': 'User Logged Out Successfully!'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def resend_otp(request):
    try:
        phone_number = request.data['phone_number']
        if phone_number is not None:
            user_obj = User.objects.get(
                phone_number=phone_number
            )
        if user_obj is not None:
            user_obj.verified = False
            user_obj.save()
            
            generated_otp = random.randint(1000, 9999)
            models.Otp.objects.filter(
                user=user_obj
            ).update(otp=generated_otp, has_used=False)
            send_otp.delay(
                phone_number=str(phone_number), otp=generated_otp 
            )
            return Response({
                'message': 'OTP sent successfully! Please verify your phone number.'
            }, status=status.HTTP_200_OK)
        return Response({
            'error': "User Not Found!"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)