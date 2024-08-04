from django.http import HttpResponse
from .utils import generate_csv_for_player_levels


def export_player_levels_to_csv(request):
    """
    Обрабатывает запрос для экспорта данных об уровнях игроков в CSV-файл.
    Returns:
        HttpResponse: HTTP-ответ с CSV-файлом для скачивания.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'
    generate_csv_for_player_levels(response)
    return response
