"""Player module containing the Player class."""

from typing import List, Dict, Tuple, Optional
import random
import copy
import math
from models.settings import Settings
from models.board import Board
from models.game_move import GameMove
from models.building_card import BuildingCard

class Player:
    """Represents a player in the game."""
    def __init__(self, player_ind: int, game_settings: Settings):
        """Initialize a player.
        
        Args:
            player_ind: Player index
            game_settings: Game settings configuration
        """
        self.player_no = player_ind
        self.game_settings = game_settings
    
    def find_move(self, board: Board, available_building_cards: List[BuildingCard], depth: int = 4) -> GameMove:
        """Find the optimal move sequence to maximize net income.
        
        Uses a look-ahead search to evaluate sequences of 4 moves and choose
        the first move of the best sequence.
        
        Args:
            board: Current game board state
            
        Returns:
            The optimal GameMove or None if no valid move found
        """
        best_move = None
        best_net_income = float('-inf')
        
        # Generate all possible first moves
        possible_moves = self._generate_possible_moves(board, available_building_cards)
        
        for move in possible_moves:
            # Simulate the move on a copy of the board
            board_copy = copy.deepcopy(board)
            self._apply_move(board_copy, move)
            
            # Recursively evaluate sequences of 3 more moves
            net_income = self._evaluate_move_sequence(board_copy, available_building_cards, depth -1)
            
            if net_income > best_net_income:
                best_net_income = net_income
                best_move = move
                
        return best_move

    def _evaluate_move_sequence(self, board: Board, available_building_cards: List[BuildingCard], depth: int) -> float:
        """Recursively evaluate sequences of moves.
        
        Args:
            board: Current board state
            depth: Number of moves left to evaluate
            
        Returns:
            Maximum net income achievable from this position
        """
        if depth == 0:
            return board.calc_player_net(self.player_no)
            
        possible_moves = self._generate_possible_moves(board, available_building_cards)
        best_net_income = float('-inf')
        
        for move in possible_moves:
            board_copy = copy.deepcopy(board)
            board_copy._apply_move(move)
            net_income = self._evaluate_move_sequence(board_copy, depth - 1)
            best_net_income = max(best_net_income, net_income)
            
        return best_net_income

    def _generate_possible_moves(self, board: Board, available_building_cards: List[BuildingCard]) -> List[GameMove]:
        """Generate all possible valid moves from the current position.
        
        Args:
            board: Current board state
            
        Returns:
            List of valid GameMove objects
        """
        moves = []
        
        # Try building placements
        for coords in board.card_index_to_location.values():
            for building_card in available_building_cards:
                move = GameMove(
                    player_ind=self.player_no,
                    building_card=building_card,
                    building_coordinate=coords,
                    employee_delta=0,
                    employee_coordinate=coords,
                    sell_price_delta=0,
                    buy_price_delta=0
                )
                if move.validate_move(board):
                    moves.append(move)

        # Try employee changes
        none_building_card = BuildingCard('None', 'none', max_players=4)
        for coords in board.card_index_to_location.values():
            for delta in [-1, 1]:
                move = GameMove(
                    player_ind=self.player_no,
                    building_card=none_building_card,
                    building_coordinate=coords,
                    employee_delta=delta,
                    employee_coordinate=coords,
                    sell_price_delta=0,
                    buy_price_delta=0
                )
                if move.validate_move(board):
                    moves.append(move)

        # Try price changes
        for sell_delta in [-1, 0, 1]:
            for buy_delta in [-1, 0, 1]:
                if sell_delta == 0 and buy_delta == 0:
                    continue
                move = GameMove(
                    player_ind=self.player_no,
                    building_card=none_building_card,
                    building_coordinate=(0,0),
                    employee_delta=0,
                    employee_coordinate=(0,0),
                    sell_price_delta=sell_delta,
                    buy_price_delta=buy_delta
                )
                if move.validate_move(board):
                    moves.append(move)

        return moves


