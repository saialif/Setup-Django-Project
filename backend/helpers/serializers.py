import uuid
from datetime import datetime

from dateutil import parser
from rest_framework import serializers

from helpers.types import bytes_to_mb


def validate_uuid(value, field_name):
    try:
        uuid.UUID(value)
    except ValueError:
        raise serializers.ValidationError(
            f"{field_name} must be a valid UUID")


class NaiveDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Parse the datetime string considering the timezone offset
        parsed_datetime = parser.parse(super().to_representation(value))
        # Convert to naive datetime
        naive_datetime = parsed_datetime.replace(tzinfo=None)
        # Return the naive datetime string without timezone info
        return naive_datetime.strftime('%d-%m-%Y %H:%M:%S')


class NaiveDateField(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            # Convert datetime to naive date
            value = value.date()
        # Return the naive date string
        return super().to_representation(value)

    def to_internal_value(self, data):
        # Convert the input data to a date object
        parsed_datetime = parser.parse(data)
        # Ensure the value is a date object
        naive_date = parsed_datetime.date()
        return super().to_internal_value(naive_date)


class BytesToMbField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise serializers.ValidationError(
                    "Invalid size format. Must be a number.")
        return bytes_to_mb(value)

    def to_internal_value(self, data):
        try:
            size_in_bytes = float(data) * 1024 * 1024
        except ValueError:
            raise serializers.ValidationError(
                "Invalid size format. Must be a number.")
        return str(int(size_in_bytes))
