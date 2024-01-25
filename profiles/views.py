from rest_framework import generics,filters
from drf_api.permissions import isOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count = Count('owner__post',distinct=True),
        followers_count = Count('owner__followed',distinct=True),
        following_count = Count('owner__following',distinct=True),

    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,

    ]
    filterset_fields =[
       'owner__following__followed__profile',
       'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [isOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer                          