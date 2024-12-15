from rest_framework import serializers
from .models import Mission, Target

class TargetSerializer(serializers.ModelSerializer):
    mission = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Target
        fields = '__all__'

    def validate(self, data):
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Не можна змінювати завершені цілі.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, required=True)

    class Meta:
        model = Mission
        fields = '__all__'

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
