from rest_framework.authtoken.models import Token

def get_or_create_token(user):
    try:
        token , _ = Token.objects.get_or_create(user=user)
        return token
    except Exception as e:
        return str(e)
    

