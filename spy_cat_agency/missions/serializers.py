from rest_framework import serializers
from .models import Mission, Target

class TargetSerializer(serializers.ModelSerializer):
    """
        Серіалізатор для моделі Target.

        Використовується для перетворення об'єктів Target у JSON-формат
        та для валідації даних цілі місії.

        Атрибути:
            mission (PrimaryKeyRelatedField): поле для відображення ідентифікатора місії,
                                              до якої належить ціль. Тільки для читання.
            Meta.model: модель Target, пов'язана із серіалізатором.
            Meta.fields: усі поля моделі Target включені у серіалізацію.

        Методи:
            validate(data): забороняє зміну даних, якщо ціль позначена як завершена.
    """
    mission = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Target
        fields = '__all__'

    def validate(self, data):
        """
            Перевіряє, чи можна змінювати дані цілі.

            Якщо ціль вже позначена як завершена, піднімається помилка валідації.

            Параметри:
                data (dict): дані, які потрібно перевірити.

            Повертає:
                dict: валідовані дані, якщо ціль не завершена.

            Піднімає:
                serializers.ValidationError: якщо ціль завершена.
        """
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Не можна змінювати завершені цілі.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    """
        Серіалізатор для моделі Mission.

        Використовується для перетворення об'єктів Mission у JSON-формат,
        а також для створення нових місій із пов'язаними цілями.

        Атрибути:
            targets (TargetSerializer): серіалізатор для цілей, пов'язаних із місією.
                                        Поле many=True вказує, що місія може мати кілька цілей.
            Meta.model: модель Mission, пов'язана із серіалізатором.
            Meta.fields: усі поля моделі Mission включені у серіалізацію.

        Методи:
            create(validated_data): створює нову місію разом із цілями.
    """
    targets = TargetSerializer(many=True, required=True)

    class Meta:
        model = Mission
        fields = '__all__'

    def create(self, validated_data):
        """
            Створює нову місію разом із пов'язаними цілями.

            Параметри:
                validated_data (dict): валідовані дані для створення місії.

            Повертає:
                Mission: створений об'єкт місії.

            Операції:
                - Вилучає дані для цілей із validated_data.
                - Створює об'єкт місії.
                - Створює об'єкти Target для кожної цілі, пов'язаної з місією.
        """
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
