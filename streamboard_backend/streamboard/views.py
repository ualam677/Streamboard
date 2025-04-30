from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Streamboard
from .serializers import StreamboardSerializer
from django.utils import timezone
import json


class StreamboardCreateView(generics.CreateAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

class StreamboardListView(generics.ListAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Streamboard.objects.filter(user=self.request.user)



class StreamboardDetailView(generics.RetrieveAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.last_view = timezone.now()
        instance.save(update_fields=['last_view'])
        return super().retrieve(request, *args, **kwargs)
    
class LatestStreamboardView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = StreamboardSerializer
    queryset = Streamboard.objects.all()

    def get(self, request):
        board = Streamboard.objects.filter(user=request.user).order_by('-last_view').first()
        if board:
            serializer = StreamboardSerializer(board)
            return Response(serializer.data)
        return Response({}, status=204)
    
class StreamboardDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Streamboard.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.last_view = timezone.now()
        instance.save(update_fields=['last_view'])
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        Save the serializer with partial updates including files like background_image.
        """
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        layout_json = request.data.get('layout_json')
        if layout_json:
            if isinstance(layout_json, str):
                try:
                    layout_json = json.loads(layout_json)
                except json.JSONDecodeError:
                    return Response({'layout_json': ['Invalid JSON']}, status=400)
            instance.layout_json = layout_json

        title = request.data.get('title')
        if title:
            instance.title = title

        if 'background_image' in request.FILES:
            instance.background_image = request.FILES['background_image']
            
        if 'logo' in request.FILES:
            instance.logo = request.FILES['logo']

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecentViewedStreamboardsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StreamboardSerializer
    queryset = Streamboard.objects.all()

    def get_queryset(self):
        return Streamboard.objects.filter(user=self.request.user).order_by('-last_view')[:3]
