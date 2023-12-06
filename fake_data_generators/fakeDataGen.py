from django.contrib.auth import get_user_model
from faker import Faker

from posts.models import Post

User = get_user_model()

def generate_fake_user(total_user):
    faker = Faker()
    for _ in range(total_user):

        full_name = faker.name()
        # make the phone number 10 digits
        phone_number = faker.phone_number()[:12]
        email = faker.email()
        password = faker.password()
        user_data = {
            'full_name': full_name,
            'phone_number': phone_number,
            'email': email,
            'password': password
        }
        generated_datas = []
        generated_datas.append(user_data)
        for user_data in generated_datas:
            User.objects.get_or_create(
                full_name=user_data['full_name'],
                phone_number=user_data['phone_number'],
                email=user_data['email'],
                password=user_data['password'],
                is_active=True,
                verified=True
            )

def generate_fake_posts(for_user, total_post):
    faker = Faker()
    for _ in range(total_post):
        title = faker.sentence()
        post_data = {
            'title': title,
            'user_id': for_user
        }
        generated_datas = []
        generated_datas.append(post_data)
        for post_data in generated_datas:
            Post.objects.get_or_create(
                title=post_data['title'],
                user_id=post_data['user_id']
            )

        