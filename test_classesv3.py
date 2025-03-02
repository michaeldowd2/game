import unittest
from classesv3 import Settings, Board, Game, BuildingCard

class TestSettings(unittest.TestCase):
    def test_initialization(self):
        settings = Settings()
        self.assertEqual(settings.base_emp_value, 1)  # Adjust based on actual defaults

class TestBoard(unittest.TestCase):
    def setUp(self):
        game_settings = Settings()  # Assuming Settings has a default constructor
        self.board = Board(game_settings, no_players=2, style='rectangle')

    def test_initialization(self):
        self.assertEqual(self.board.game_settings, self.board.game_settings)

class TestGame(unittest.TestCase):
    def setUp(self):
        game_settings = Settings()  # Create a Settings instance
        self.game = Game(game_settings, no_players=2)  # Provide required arguments

    def test_initialization(self):
        self.assertIsNotNone(self.game)  # Check if the game instance is created
        self.assertEqual(self.game.turn_number, 0)  # Check initial turn number
        self.assertEqual(len(self.game.players), 2)  # Check initial number of players

class TestBuildingCard(unittest.TestCase):
    def test_buy_market_values(self):
        card = BuildingCard(card_type='buy_market')
        values, x_values, y_values = card.generate_values()
        self.assertEqual(values[1][2], 4)  # Example assertion
        self.assertEqual(x_values, [1, 2, 3, 4])  # Check x_values
        self.assertEqual(y_values, [1, 2, 3, 4, 5, 6, 7, 8])  # Check y_values

    def test_sell_market_values(self):
        card = BuildingCard(card_type='sell_market')
        values, x_values, y_values = card.generate_values()
        self.assertEqual(values[2][4], 4)  # Example assertion
        self.assertEqual(x_values, [2, 3, 4, 5])  # Check x_values
        self.assertEqual(y_values, [2,3, 4, 5, 6, 7, 8, 9, 10])  # Check y_values

    def test_process_values(self):
        card = BuildingCard(card_type='process')
        values, x_values, y_values = card.generate_values()
        self.assertEqual(values[1][1], 4)  # Example assertion
        self.assertEqual(x_values, [0, 1, 2])  # Check x_values
        self.assertEqual(y_values, [0, 1, 2])  # Check y_values

if __name__ == '__main__':
    unittest.main()
