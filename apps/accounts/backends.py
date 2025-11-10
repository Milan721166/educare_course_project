from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class RoleBasedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                # For teachers, check if they are approved
                if user.role == 'teacher' and not user.is_approved:
                    return None
                return user
        except UserModel.DoesNotExist:
            return None