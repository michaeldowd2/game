"""Test suite for the game models."""

import unittest
from models import Settings, Board, Game, BuildingCard

class TestSettings(unittest.TestCase):
    """Test cases for the Settings class."""
    
    def test_initialization(self):
        """Test initialization of Settings with default values."""
        settings = Settings()
        self.assertEqual(settings.base_emp_value, 1)
        self.assertEqual(settings.emp_cost, 1)

class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.settings = Settings()
        self.board = Board(self.settings, no_players=2, style='rectangle')

    def test_initialization(self):
        """Test initialization of Board with default values."""
        self.assertEqual(self.board.game_settings, self.settings)
        self.assertEqual(self.board.no_players, 2)
        self.assertIsNotNone(self.board.mask)
        self.assertIsNotNone(self.board.cards)
        self.assertIsNotNone(self.board.player_bud_arrays)
        self.assertIsNotNone(self.board.player_emp_arrays)

    def test_calc_player_net(self):
        """Test calculation of player net worth."""
        net = self.board.calc_player_net(0)
        self.assertIsInstance(net, (int, float))


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.settings = Settings()
        self.game = Game(self.settings, no_players=2)

    def test_initialization(self):
        """Test initialization of Game with default values."""
        self.assertIsNotNone(self.game)
        self.assertEqual(self.game.turn_number, 0)
        self.assertEqual(len(self.game.players), 2)
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.building_cards)

    def test_building_cards_initialization(self):
        """Test initialization of building card decks."""
        self.assertIn('buy_market', self.game.building_cards)
        self.assertIn('sell_market', self.game.building_cards)
        self.assertIn('process', self.game.building_cards)
        self.assertIn('hq', self.game.building_cards)


class TestBuildingCard(unittest.TestCase):
    """Test cases for the BuildingCard class."""
    
    def test_buy_market_values(self):
        """Test value generation for buy market cards."""
        card = BuildingCard(
            name='Buy Market',
            card_type='buy_market',
            x_name='Total Spend',
            y_name='Player Spend',
            max_players=2,
            max_output=5
        )
        values, x_values, y_values = card.generate_values()
        self.assertEqual(len(x_values), 4)
        self.assertEqual(len(y_values), 8)
        self.assertGreaterEqual(values[1][2], 0)

    def test_sell_market_values(self):
        """Test value generation for sell market cards."""
        card = BuildingCard(
            name='Sell Market',
            card_type='sell_market',
            x_name='Total Price',
            y_name='Player Price',
            max_players=2,
            max_output=5
        )
        values, x_values, y_values = card.generate_values()
        self.assertEqual(len(x_values), 4)
        self.assertEqual(len(y_values), 9)
        self.assertGreaterEqual(values[2][4], 0)

    def test_process_values(self):
        """Test value generation for process cards."""
        card = BuildingCard(
            name='Process',
            card_type='process',
            x_name='Connected Buy',
            y_name='Connected Sell',
            max_players=1,
            max_output=10
        )
        values, x_values, y_values = card.generate_values()
        self.assertEqual(len(x_values), 3)
        self.assertEqual(len(y_values), 3)
        self.assertGreaterEqual(values[1][1], 0)


if __name__ == '__main__':
    unittest.main()
