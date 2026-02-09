from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication

class DefaultUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        user = User.objects.first()
        if not user:
            # Create a default user if none exists
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        return (user, None)
