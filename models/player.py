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
    
    def find_best_move(self, board: Board, available_building_cards: List[BuildingCard], max_depth: int = 4, moves_to_try: int = -1, debug_level: int = 0, current_depth: int = 0) -> GameMove:
        """Find the optimal move sequence to maximize net income.
        
        Uses a look-ahead search to evaluate sequences of 4 moves and choose
        the first move of the best sequence.
        
        Args:
            board: Current game board state
            available_building_cards: List of available building cards
            max_depth: Maximum depth of look-ahead search
            moves_to_try: Number of moves to try
            debug_level: Debug level
            current_depth: Current depth of search
            
        Returns:
            The optimal GameMove or None if no valid move found
        """
        pstr = ''
        for d in range(current_depth): pstr += '  ' 

        if current_depth == max_depth:
            show_net_calc = False
            if debug_level > 1: show_net_calc = True

            net = board.calc_player_net(self.player_no, show_net_calc)
            if debug_level > 0: print('net: ' + str(net))
            return None, net
        
        best_move, best_net_income = None, float('-inf')
        all_possible_moves = self._generate_possible_moves(board, available_building_cards)
        possible_moves = all_possible_moves[:moves_to_try] if moves_to_try > 0 else all_possible_moves

        for move in possible_moves:
            board_copy = copy.deepcopy(board)
            move.apply(board_copy)
            if debug_level > 0: print(pstr + str(current_depth) + '_move: ' + str(move))
            if debug_level > 1: print(board_copy)
            _, net_income = self.find_best_move(board_copy, available_building_cards, max_depth, moves_to_try, debug_level, current_depth + 1)
            
            if net_income > best_net_income:
                best_net_income = net_income
                best_move = move
                
        return best_move, best_net_income

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


