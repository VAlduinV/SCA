from django.shortcuts import render
from rest_framework import viewsets
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign(self, request, pk=None):
        """
        Assigns a cat to a mission.
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
        Marks a mission as completed.
        """
        mission = self.get_object()
        if mission.is_completed:
            return Response({"detail": "Mission already completed"}, status=status.HTTP_400_BAD_REQUEST)
        mission.is_completed = True
        mission.save()
        return Response({"detail": f"Mission {mission.id} marked as completed"})


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        target = self.get_object()
        if target.is_completed:
            return Response({"detail": "Target already completed"}, status=status.HTTP_400_BAD_REQUEST)
        target.is_completed = True
        target.save()
        return Response({"detail": f"Target {target.name} marked as completed"})

    @action(detail=True, methods=['patch'])
    def notes(self, request, pk=None):
        target = self.get_object()
        if target.is_completed:
            return Response({"detail": "Cannot update notes for a completed target."},
                            status=status.HTTP_400_BAD_REQUEST)
        target.notes = request.data.get('notes', '')
        target.save()
        return Response({"detail": "Notes updated successfully."})