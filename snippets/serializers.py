from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source ='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'title', 'code', 'lineos',
                  'language', 'style', 'owner',) 
    # could have also used Charfield with read_only=True as the argument
    # this owner reflects the change that we made to the view where the snippets
    # are saved by owner


#below will show the transformed model only to a user that's signed in
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
    many=True, queryset=Snippet.objects.all())

    class Meta:
        model  = User
        fields = ('url','id','username','snippets')
    

# A Serializer transforms model instances into JSON. 
# Consider that the end result of a traditional website is a page of HTML, CSS, 
# and content from the database. But an API doesn't care about that: 
# it's only raw data at endpoints, which means JSON, 
# and accompanying HTTP verbs that tell the API what actions can be taken.