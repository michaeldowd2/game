"""Game move module containing the GameMove class."""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from models.board import Board

@dataclass
class GameMove:
    """Represents a game move.
    
    Attributes:
        player_ind: Player index
        building_type: Type of building
        building_coordinate: Coordinate of building
        employee_delta: Change in employee count
        employee_coordinate: Coordinate of employee
        sell_price_delta: Change in sell price
        buy_price_delta: Change in buy price
    """
    player_ind: int
    building_type: str
    building_coordinate: Tuple[int, int]
    employee_delta: int
    employee_coordinate: Tuple[int, int]
    sell_price_delta: int
    buy_price_delta: int
    
    def __post_init__(self):
        """Validate values after initialization."""
        allowed_building_types = ['sell_market', 'process', 'buy_market', 'hq']
        if self.building_type not in allowed_building_types:
            raise ValueError(f"building type must be one of {allowed_building_types}")
        
        # players can only add or remove 1 employee per turn
        if self.employee_delta not in [-1,0,1]:
            raise ValueError(f"employee delta must be one of {-1,0,1}")
        
        # players can only increase or decrease the sell price by one per turn
        if self.sell_price_delta not in [-1,0,1]:
            raise ValueError(f"sell price delta must be one of {-1,0,1}")
        
        # players can only increase or decrease the buy price by one per turn
        if self.buy_price_delta not in [-1,0,1]:
            raise ValueError(f"buy price delta must be one of {-1,0,1}")

    def validate_move(self, board: Board) -> bool:
        """Validate the move against the board state.
        Args:
            board: Board state
        
        Returns:
            True if the move is valid, False otherwise
        """
        if not board.validate_building_placement(self.player_ind, self.building_type, self.building_coordinate[0], self.building_coordinate[1]):
            return False
        if not board.validate_employee_delta(self.player_ind, self.employee_delta, self.employee_coordinate[0], self.employee_coordinate[1]):
            return False
        if not board.validate_sell_price_delta(self.player_ind, self.sell_price_delta):
            return False
        if not board.validate_buy_price_delta(self.player_ind, self.buy_price_delta):
            return False

        return True