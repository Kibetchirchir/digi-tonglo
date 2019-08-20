from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


def validate_password():
    """
    Validates if a string has on alpha-numeric characters
    :return: None or Message that a string is not valid
    """
    return RegexValidator(
        r'^[0-9a-zA-Z]+$',
        "Only numbers and letters are allowed in password")


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[validate_password()],
        error_messages={
            "min_length": "Please ensure that your password has more than 8 characters",
            "blank": "A password is required to complete registration",
            "required": "A password is required to complete registration"
        }
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            "username": {
                "error_messages": {
                    "required": "A username is required to complete registration",
                    "blank": "A username is required to complete registration"
                },
                "validators":
                    [UniqueValidator(queryset=User.objects.all(),
                                     message="Username is already assigned to another user")]
            },
            "email": {
                "error_messages": {
                    "required": "Email must be provided to complete registration",
                    "blank": "Email must be provided to complete registration",
                    "invalid": "The provided email is invalid"
                },
                "validators":
                    [UniqueValidator(queryset=User.objects.all(),
                                     message="Email is already registered to another user")]
            }
        }

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)
