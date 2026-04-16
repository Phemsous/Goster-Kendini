from .models import User, Profile


def create_user_service(username, password, role='artist', **extra_fields):
    extra_fields.pop('confirm_password', None)

    user = User(username=username, role=role, **extra_fields)
    user.set_password(password)
    user.save()

    Profile.objects.create(
        user=user,
        full_name=username
    )

    return user