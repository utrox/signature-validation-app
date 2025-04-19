from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address', 'phone', 'date_of_birth', 'bank_account_number']
