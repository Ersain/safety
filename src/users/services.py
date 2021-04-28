from .models import User


class UserServices:
    @staticmethod
    def reset_password(email, password):
        user = User.objects.filter(email=email)
        if not user.exists():
            return
        user = user.first()
        user.set_password(password)
        user.save()
