from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        print("Start _create_user")
        if not username:
            if not email and not phone:
                raise ValueError('The given email/phone must be set')

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(
                email=email,
                username=username,
                **extra_fields
            )

        if phone:
            if not username:
                username = phone

            user = self.model(
                username=username,
                phone=phone,
                **extra_fields
            )
        
        # проверяем является ли пользователь
        # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                username=phone,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        print("Start create_user")
        extra_fields.setdefault('is_superuser', False)
        password = "123"
        return self._create_user(phone=phone, password=password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username=phone,
            phone=phone,
            password=password,
            **extra_fields
        )