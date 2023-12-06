from .fakeDataGen import generate_fake_user
from rest_framework.decorators import api_view
from rest_framework import response

@api_view(['GET'])
def generateFakeUser(request, users):
    generate_fake_user(total_user=users)
    return response.Response({
        f"{users} users were created!"
    })
