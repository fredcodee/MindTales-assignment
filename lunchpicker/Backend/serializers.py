from rest_framework import serializers
from .models import Restaurant, Menu, Vote
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},  # Password must be provided and write-only
            'email': {'required': True}, 
            'username': {'required': True}  
        }
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__' 
        
        

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__' 
        
        

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def validate_points(self, value):
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Points must be between 1 and 3.")
        return value


