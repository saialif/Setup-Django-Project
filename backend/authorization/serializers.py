from rest_framework import serializers


class ValidateLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate_username_or_email(self, value):
        if not value:
            raise serializers.ValidationError("Username/email is required.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        return value

    def validate(self, data):
        username = data.get('username_or_email')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                "Both username/email and password are required.")

        return data
