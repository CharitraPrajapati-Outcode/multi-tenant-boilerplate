from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from ...models import User
from ...constants import SUPER_ADMIN


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # remove any existing groups
        super_admin = Group.objects.create(name=SUPER_ADMIN)

        password = "asd123!@#"
        users = [
            {
            'first_name': 'Super',
            'last_name': 'Admin',
            'email': 'admin@domain.com',
            'is_active': True
            }
        ]
        new_password = "admin@123"

        for user_data in users:
            user = User.objects.create(**user_data)
            user.set_password(password)
            user.save()
            super_admin.user_set.add(user)
            
        print('Successfully loaded users!')
