from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from posts.models import Post, Comment

from . import comments_serializers

class CommentView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = comments_serializers.CommentsSerializers

    def get(self, request, post_id : int, *args, **kwargs):
        try:
            if post_id is not None:
                post_objs = Post.objects.filter(id=post_id)
                if post_objs.exists():
                    comments = Comment.objects.filter(post_id=post_id)
                    serializer = self.serializer_class(comments, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "post id is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context = {'request': request})
            if serializer.is_valid():
                post_id = serializer.validated_data['post'].id
                post_objs = Post.objects.filter(id=post_id)
                if post_objs.exists():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, comment_id : int, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context = {'request': request})
            if serializer.is_valid():
                post_objs = Comment.objects.filter(id=comment_id, user=request.user)
                if post_objs.exists():
                    post_objs.update(comment=serializer.validated_data['comment'])
                    return Response({
                        "edited_comment": serializer.validated_data['comment']
                    }, status=status.HTTP_200_OK)
                return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, comment_id : int, *args, **kwargs):
        try:
            post_objs = Comment.objects.filter(id=comment_id, user=request.user)
            if post_objs.exists():
                post_objs.delete()
                return Response({
                    "message": "comment deleted!"
                }, status=status.HTTP_200_OK)
            return Response({"message": "comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)