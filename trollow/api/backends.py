from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        UserModel = get_user_model()
        try:
            # For admin flow
            if username:
                user = UserModel.objects.get(email=username)
            # For standard login
            elif email:
                user = UserModel.objects.get(email=email)
            else:
                raise UserModel.DoesNotExist
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None