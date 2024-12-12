from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Player
from .serializer import PlayerSerializer
from django.http import JsonResponse

def test_view(request):
    return JsonResponse({"message": "Hello from the backend!"})

@api_view(['GET'])
def player_list(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)