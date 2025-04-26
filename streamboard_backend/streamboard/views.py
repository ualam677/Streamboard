from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Streamboard
from .serializers import StreamboardSerializer

class StreamboardCreateView(generics.CreateAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticated]


class StreamboardDetailView(generics.RetrieveUpdateAPIView):
    queryset = Streamboard.objects.all()
    serializer_class = StreamboardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = request.data.get('fields', [])

        instance.layout_json = fields
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)