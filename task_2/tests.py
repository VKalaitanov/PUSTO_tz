from django.test import TestCase
from django.urls import reverse
from io import StringIO
import csv
from django.utils import timezone
from .models import Player, Level, Prize, PlayerLevel, LevelPrize


class PlayerLevelTestCase(TestCase):

    def setUp(self):
        self.player = Player.objects.create(player_id="player1")
        self.level = Level.objects.create(title="Level 1", order=1)
        self.prize1 = Prize.objects.create(title="Prize 1")
        self.prize2 = Prize.objects.create(title="Prize 2")
        self.level_prize1 = LevelPrize.objects.create(level=self.level, prize=self.prize1, received=timezone.now())
        self.level_prize2 = LevelPrize.objects.create(level=self.level, prize=self.prize2, received=timezone.now())
        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            completed=timezone.now(),
            is_completed=True,
            score=100
        )

    def test_export_player_levels_to_csv(self):
        """
        Проверяет, что данные экспортируются в CSV файл правильно.
        """
        response = self.client.get(reverse('export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="player_levels.csv"')

        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)

        self.assertEqual(rows[0], ['Player ID', 'Level Title', 'Completed', 'Prize Title'])
        self.assertEqual(rows[1], ['player1', 'Level 1', 'True', 'Prize 1, Prize 2'])

    def test_export_no_player_levels(self):
        """
        Проверяет, что происходит правильное поведение, когда нет записей PlayerLevel.
        """
        PlayerLevel.objects.all().delete()  # Удаляем все записи PlayerLevel
        response = self.client.get(reverse('export_csv'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)

        self.assertEqual(rows, [['Player ID', 'Level Title', 'Completed', 'Prize Title']])

    def test_export_multiple_prizes(self):
        """
        Проверяет, что при наличии нескольких призов для уровня все призы экспортируются в CSV.
        """
        self.assertEqual(PlayerLevel.objects.count(), 1)
        response = self.client.get(reverse('export_csv'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)

        # Проверяем, что оба приза экспортируются
        self.assertEqual(rows[1], ['player1', 'Level 1', 'True', 'Prize 1, Prize 2'])
