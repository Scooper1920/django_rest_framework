from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .permissions import IsOwnerOrReadOnly
from .models import Snippet
from .serializers import SnippetSerializer,UserSerializer


@api_view(['GET'])
def api_root(request,format =None):
    return Response({
        'users':reverse('user-list',request=request, format=format),
        'snippets':reverse('snippet-list',request=request, format=format)
    })


# Create your views here.
class SnippetList(generics.ListCreateAPIView):
    queryset            = Snippet.objects.all()
    serializer_class    = SnippetSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)
#they knew to import that there because those are the definitions
# that a listCreateAPIview requires 
# https://www.django-rest-framework.org/api-guide/generic-views/
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
# ok so line 18 automatically associates the logged in user with the snippet
# instance so now THIS is how the the instance is saved >>go to serializers.py

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset            = Snippet.objects.all()
    serializer_class    = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
# Here and line 14 we will use IsAuthenticatedOrReadOnly to ensure that authenticated 
# requests have read-write access and unauthenticated requests only 
# have read-only access.

class UserList(generics.ListAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer


class SnippetHighlight(generics.GenericAPIView): 
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
