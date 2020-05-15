from rest_framework import viewsets
from . import models, serializers


class UserViewset(viewsets.ModelViewSet):
    # queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        qs = models.User.objects.all()
        return qs
