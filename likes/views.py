from rest_framework import generics,permissions
from drf_api.permissions import isOwnerOrReadOnly
from likes.serializers import LikeSerializer
from likes.models import Like


class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self,serializer):
        serializer.save(owner =self.request.user)
