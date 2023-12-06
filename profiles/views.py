from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from . import models, serializers

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


class ProfileView(generics.GenericAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None, *args, **kwargs):
        try:
            user_obj = models.User.objects.filter(id=pk).first()
            profile_obj = models.Profile.objects.filter(user=user_obj).first()
            if profile_obj is not None:
                serializer = self.serializer_class(profile_obj)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            return Response(
                {"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        try:
            profile_obj = models.Profile.objects.filter(user=request.user).first()
            if profile_obj is not None:
                serializer = self.serializer_class(profile_obj, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": "Profile updated successfully",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CoverPhotoView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CoverPhotoSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            return Response(
                {"cover_photo": user.cover_photo.url if user.cover_photo else None},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializers = self.serializer_class(data=request.data)
            if serializers.is_valid():
                cover_photo = serializers.validated_data["cover_photo"]
                user_obj = models.User.objects.filter(id=request.user.id).first()
                user_obj.cover_photo.delete()
                user_obj.cover_photo = cover_photo
                user_obj.save()
                return Response(
                    {"message": "Cover photo uploaded successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    try:
        user = request.user
        profile = models.Profile.objects.filter(user=user).first()
        if profile is not None:
            serializer = serializers.ProfileSerializer(profile)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )