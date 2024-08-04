from django.test import TestCase
from .models import Player, Boost


class PlayerModelTests(TestCase):
    def test_first_login_is_set_on_save(self):
        """
        Проверяет, что поле `first_login` устанавливается при первом сохранении объекта `Player`.
        """
        player = Player.objects.create(username='testplayer')
        # Проверяем, что поле `first_login` не является None после сохранения
        self.assertIsNotNone(player.first_login)

    def test_add_points(self):
        """
        Проверяет, что метод `add_points` корректно добавляет
        баллы к текущему количеству баллов игрока.
        """
        player = Player.objects.create(username='testplayer', points=10)
        player.add_points(5)
        # Проверяем, что количество баллов увеличилось на 5
        self.assertEqual(player.points, 15)

    def test_add_boost(self):
        """
        Проверяет, что метод `add_boost` корректно добавляет буст игроку.
        """
        player = Player.objects.create(username='testplayer')
        player.add_boost(name='Speed Boost', description='Increases speed by 20%')
        # Проверяем, что у игрока появился один буст
        self.assertEqual(player.boosts.count(), 1)
        boost = player.boosts.first()
        # Проверяем, что имя, описание и флаг manually_awarded буста соответствуют ожидаемым значениям
        self.assertEqual(boost.name, 'Speed Boost')
        self.assertEqual(boost.description, 'Increases speed by 20%')
        self.assertFalse(boost.manually_awarded)


class BoostModelTests(TestCase):
    def test_boost_creation(self):
        """
        Проверяет, что буст корректно создается и связывается с игроком.
        """
        player = Player.objects.create(username='testplayer')
        boost = Boost.objects.create(
            player=player,
            name='Speed Boost',
            description='Increases speed by 20%'
        )
        # Проверяем, что буст связан с правильным игроком
        self.assertEqual(boost.player, player)
        # Проверяем, что имя и описание буста соответствуют ожидаемым значениям
        self.assertEqual(boost.name, 'Speed Boost')
        self.assertEqual(boost.description, 'Increases speed by 20%')
        # Проверяем, что флаг manually_awarded имеет значение False по умолчанию
        self.assertFalse(boost.manually_awarded)
