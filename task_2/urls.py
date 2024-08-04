from django.urls import path
from .views import export_player_levels_to_csv

urlpatterns = [
    path('export-csv/', export_player_levels_to_csv, name='export_csv'),
]
