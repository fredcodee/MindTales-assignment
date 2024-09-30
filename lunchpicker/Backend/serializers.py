from rest_framework import serializers
from .models import Restaurant, Menu, Vote

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


