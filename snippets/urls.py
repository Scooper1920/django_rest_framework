from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
#this new urls.py presents an ENDPOINT and will connect to the project level
# urls.py

urlpatterns = [
    path('snippets/', views.SnippetList.as_view(),name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(),name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',views.SnippetHighlight.as_view(), name='snippet-highlight'), 
    path('users/',views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name ='user-detail'),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# Including format_suffix_patterns is an optional choice 
# that provides a simple, DRY way to refer to a specific file format 
# for a URL endpoint. It means our API will be able to handle 
# URls such as http://example.com/api/items/4.json rather than 
# just http://example.com/api/items/4.

