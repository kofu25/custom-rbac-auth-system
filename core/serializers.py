from rest_framework import serializers
from .models import User, AccessRule, Role

class UserRegisterSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password_hash', 'password_repeat']
        extra_kwargs = {'password_hash': {'write_only': True}}

    def validate(self, data):
        if data['password_hash'] != data['password_repeat']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email']

class AccessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = '__all__'