from django.urls import path
from .views import *

urlpatterns = [
    path('distance/', distance_view, name='distance'),
    path('longest/', longest_view, name='longest'),
    path('shortest/', shortest_view, name='shortest'),
    path('add/', add_node_view, name='add_node'),
    path('tree-data/', tree_data, name='tree_data'),
]