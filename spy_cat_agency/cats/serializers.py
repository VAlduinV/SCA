from rest_framework import serializers
from .models import Cat
import requests


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'

    def validate_breed(self, value):
        # Інтеграція з TheCatAPI для перевірки породи
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        if response.status_code != 200:
            raise serializers.ValidationError("Не вдалося перевірити породу кота.")

        breeds = [breed['name'] for breed in response.json()]
        if value not in breeds:
            raise serializers.ValidationError(f"Порода '{value}' не знайдена в TheCatAPI.")
        return value
