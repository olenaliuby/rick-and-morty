import random

from django.db.models import QuerySet
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


def get_random_character() -> Character:
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    return Character.objects.get(pk=random_pk)


@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    """Get random character from Rick & Morty world"""
    random_character = get_random_character()
    serializer = CharacterSerializer(random_character)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
