import csv
from django.http import HttpResponse
from .models import PlayerLevel, LevelPrize, PlayerPrize


def assign_prize_to_player_level(player_level: PlayerLevel) -> None:
    """
    Присваивает призы игроку за прохождение уровня.
    Если уровень пройден, создает запись в PlayerPrize для каждого приза, связанного с уровнем.

    Объект PlayerLevel, который содержит информацию о прохождении уровня.
    """
    if player_level.is_completed:
        level_prizes = LevelPrize.objects.filter(level=player_level.level)
        for level_prize in level_prizes:
            PlayerPrize.objects.get_or_create(
                player=player_level.player,
                prize=level_prize.prize,
                defaults={'awarded': player_level.completed}  # Устанавливаем дату вручения
            )


def generate_csv_for_player_levels(response: HttpResponse) -> None:
    """
    Генерирует CSV-файл с данными об уровнях и призах для игрока и записывает его в ответ.
    Данные включают ID игрока, название уровня, статус завершения уровня и полученные призы.

    response (HttpResponse): HTTP-ответ, в который записывается CSV-файл.
    """
    writer = csv.writer(response)
    writer.writerow(['Player ID', 'Level Title', 'Completed', 'Prize Title'])

    player_levels = PlayerLevel.objects.select_related('player', 'level').prefetch_related(
        'level__levelprize_set'
    )

    for player_level in player_levels:
        level_prizes = [lp.prize.title for lp in player_level.level.levelprize_set.all()]
        writer.writerow([
            player_level.player.player_id,
            player_level.level.title,
            player_level.is_completed,
            ", ".join(level_prizes)
        ])
