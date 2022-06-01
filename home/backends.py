from home.models import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
          print("User is in get_user")
          return User.objects.get(pk=user_id)
        except User.DoesNotExist:
          print("User doesn't exist in get_user")
          return None

    def authenticate(self, request, username, password):
        print("In backend")
        print(username)
        print(password)
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )
            print("User is found!")
        except User.DoesNotExist:
            print("User in backend is not found")
            return None

        if user.check_password(password):
            print("User was returned")
            return user
        else:
            print("Problem with password")
            return None