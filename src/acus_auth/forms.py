from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser, User


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True) -> AbstractBaseUser | None:
        user = super(RegisterUser, self).save(commit=False)
        if commit:
            user.save()
        return user
