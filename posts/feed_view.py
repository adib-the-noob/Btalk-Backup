from rest_framework import status, generics
from rest_framework.response import Response
from . import models, serializers
from friends.models import Contacts
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import random
# from rest_framework.pagination import PageNumberPagination
from posts.feed_paginator import FeedPaginator 

class FeedView(generics.GenericAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = FeedPaginator

    def get(self, request, *args, **kwargs):
        try:
            # load all users from contact models
            # and get the ids of the users
            users = Contacts.objects.get(user=request.user)
            user_ids = [user["id"] for user in users.contacts]

            # load all posts from the users
            # and filter the posts by privacy
            posts = models.Post.objects.filter(
                Q(user__in=user_ids)
                | Q(user=request.user) & Q(privacy__in=["public", "friends"])
            ).exclude(privacy="only me").order_by("-created_at")

            shuffled_posts = list(posts)
            random.shuffle(shuffled_posts)

            # paginate the posts
            paginator = self.pagination_class()
            paginator.page_size = 20
            result_page = paginator.paginate_queryset(shuffled_posts, request)
            
            # Instead of returning an empty array, check if result_page is None and return it as is
            if result_page is None:
                return Response(None, status=status.HTTP_200_OK)

            serializer = serializers.PostSerializer(
                result_page, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                [], status=status.HTTP_200_OK
            )