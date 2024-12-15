from rest_framework import serializers
from .models import Cat
import requests


class CatSerializer(serializers.ModelSerializer):
    """
        Серіалізатор для моделі Cat.

        Цей серіалізатор використовується для перетворення даних моделі Cat
        у JSON-формат і назад, а також для валідації даних.

        Основні функції:
        - Забезпечує CRUD-операції для моделі Cat.
        - Перевіряє, чи порода кота існує в TheCatAPI під час створення або оновлення запису.

        Атрибути:
            model (Model): модель Cat, пов'язана із цим серіалізатором.
            fields (str): всі поля моделі Cat включені у серіалізацію.
    """
    class Meta:
        model = Cat
        fields = '__all__'

    def validate_breed(self, value):
        """
            Перевіряє, чи вказана порода кота існує у TheCatAPI.

            Надсилається запит до TheCatAPI, щоб отримати список доступних порід.
            Якщо порода, вказана в `value`, не знайдена у відповіді API, піднімається помилка валідації.

            Параметри:
                value (str): порода кота, яку потрібно перевірити.

            Повертає:
                str: вказана порода, якщо вона успішно пройшла валідацію.

            Піднімає:
                serializers.ValidationError: якщо API недоступний або порода не знайдена.
        """

        # Інтеграція з TheCatAPI для перевірки породи
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        if response.status_code != 200:
            raise serializers.ValidationError("Не вдалося перевірити породу кота.")

        breeds = [breed['name'] for breed in response.json()]
        if value not in breeds:
            raise serializers.ValidationError(f"Порода '{value}' не знайдена в TheCatAPI.")
        return value
