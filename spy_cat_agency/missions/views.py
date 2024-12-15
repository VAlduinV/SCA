from django.shortcuts import render
from rest_framework import viewsets
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class MissionViewSet(viewsets.ModelViewSet):
    """
        ViewSet для управління місіями.

        Цей ViewSet забезпечує CRUD-операції для моделі Mission, а також додаткові дії:
        - Призначення кота на місію (`assign`).
        - Позначення місії як завершеної (`complete`).

        Атрибути:
            queryset (QuerySet): вибірка всіх об'єктів Mission.
            serializer_class (Serializer): серіалізатор для моделі Mission.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign(self, request, pk=None):
        """
            Призначає кота на місію.

            Ця дія дозволяє призначити кота на місію, вказавши `cat_id` у тілі запиту.

            Параметри:
                request (Request): запит із даними (повинен містити `cat_id`).
                pk (int): первинний ключ місії.

            Повертає:
                Response: відповідь із повідомленням про успішне призначення або помилку.

            Випадки помилок:
                - Відсутній параметр `cat_id`.
        """
        mission = self.get_object()
        cat_id = request.data.get('cat_id')
        if not cat_id:
            return Response({"detail": "cat_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        mission.cat_id = cat_id
        mission.save()
        return Response({"detail": f"Mission {mission.id} assigned to Cat {cat_id}"})

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete(self, request, pk=None):
        """
            Позначає місію як завершену.

            Ця дія дозволяє позначити місію як завершену, якщо вона ще не завершена.

            Параметри:
                request (Request): запит.
                pk (int): первинний ключ місії.

            Повертає:
                Response: відповідь із повідомленням про успішне завершення або помилку.

            Випадки помилок:
                - Місія вже позначена як завершена.
        """
        mission = self.get_object()
        if mission.is_completed:
            return Response({"detail": "Mission already completed"}, status=status.HTTP_400_BAD_REQUEST)
        mission.is_completed = True
        mission.save()
        return Response({"detail": f"Mission {mission.id} marked as completed"})


class TargetViewSet(viewsets.ModelViewSet):
    """
        ViewSet для управління цілями.

        Цей ViewSet забезпечує CRUD-операції для моделі Target, а також додаткові дії:
        - Позначення цілі як завершеної (`complete`).
        - Оновлення нотаток для цілі (`notes`).

        Атрибути:
            queryset (QuerySet): вибірка всіх об'єктів Target.
            serializer_class (Serializer): серіалізатор для моделі Target.
    """
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """
            Позначає ціль як завершену.

            Параметри:
                request (Request): запит.
                pk (int): первинний ключ цілі.

            Повертає:
                Response: відповідь із повідомленням про успішне завершення або помилку.

            Випадки помилок:
                - Ціль уже позначена як завершена.
        """
        target = self.get_object()
        if target.is_completed:
            return Response({"detail": "Target already completed"}, status=status.HTTP_400_BAD_REQUEST)
        target.is_completed = True
        target.save()
        return Response({"detail": f"Target {target.name} marked as completed"})

    @action(detail=True, methods=['patch'])
    def notes(self, request, pk=None):
        """
            Оновлює нотатки для цілі.

            Параметри:
                request (Request): запит із даними (повинен містити `notes`).
                pk (int): первинний ключ цілі.

            Повертає:
                Response: відповідь із повідомленням про успішне оновлення нотаток або помилку.

            Випадки помилок:
                - Ціль позначена як завершена (заборонено оновлювати нотатки для завершених цілей).
        """
        target = self.get_object()
        if target.is_completed:
            return Response({"detail": "Cannot update notes for a completed target."},
                            status=status.HTTP_400_BAD_REQUEST)
        target.notes = request.data.get('notes', '')
        target.save()
        return Response({"detail": "Notes updated successfully."})
