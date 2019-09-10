from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth import authenticate


def validate_password():
    """
    Validates if a string has on alpha-numeric characters
    :return: None or Message that a string is not valid
    """
    return RegexValidator(
        r'^[0-9a-zA-Z]+$',
        "Only numbers and letters are allowed in password")


def validate_phone():
    return RegexValidator(
        r'^07|254',
        "The phone number is should start with 07 or 254(the code)"
    )


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

    phone_number = serializers.CharField(max_length=12, min_length=10,
                                         validators=[validate_phone()])

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'phone_number']
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


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'Invalid email or password provided.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
