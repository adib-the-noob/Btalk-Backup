from .fakeDataGen import generate_fake_posts
from rest_framework.decorators import api_view
from rest_framework import response

@api_view(['GET'])
def generateFakePosts(request, user, total_post):
    generated_posts = generate_fake_posts(for_user=user, total_post=total_post)
    return response.Response({
        "message": f"{total_post} posts were created, for user {user}!",
    })
