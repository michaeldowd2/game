"""Game move module containing the GameMove class."""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from models.board import Board
from models.building_card import BuildingCard
import copy

@dataclass
class GameMove:
    """Represents a game move.
    
    Attributes:
        player_ind: Player index
        building_card: Building card
        building_coordinate: Coordinate of building
        employee_delta: Change in employee count
        employee_coordinate: Coordinate of employee
        sell_price_delta: Change in sell price
        buy_price_delta: Change in buy price
        current_net: current player net
    """
    player_ind: int
    building_card: BuildingCard
    building_coordinate: Tuple[int, int]
    employee_delta: int
    employee_coordinate: Tuple[int, int]
    sell_price_delta: int
    buy_price_delta: int

    def __post_init__(self):
        """Validate values after initialization."""
        #allowed_building_types = ['sell_market', 'process', 'buy_market', 'hq']
        #if self.building_type not in allowed_building_types:
        #    raise ValueError(f"building type must be one of {allowed_building_types}")
        
        # players can only add or remove 1 employee per turn
        if self.employee_delta not in [-1,0,1]:
            raise ValueError(f"employee delta must be one of {-1,0,1}")
        
        # players can only increase or decrease the sell price by one per turn
        if self.sell_price_delta not in [-1,0,1]:
            raise ValueError(f"sell price delta must be one of {-1,0,1}")
        
        # players can only increase or decrease the buy price by one per turn
        if self.buy_price_delta not in [-1,0,1]:
            raise ValueError(f"buy price delta must be one of {-1,0,1}")

    def __str__(self) -> str:
        out = f"P{self.player_ind}"
        out += f"B{self.building_card}{self.building_coordinate[0]}{self.building_coordinate[1]}"
        sym = "+"
        if self.employee_delta < 0: sym = "-"
        out += f"E{sym}{abs(self.employee_delta)}{self.employee_coordinate[0]}{self.employee_coordinate[1]}"
        sym = "+"
        if self.sell_price_delta < 0: sym = "-"
        out += f"S{sym}{abs(self.sell_price_delta)}"
        sym = "+"
        if self.buy_price_delta < 0: sym = "-"
        out += f"B{sym}{abs(self.buy_price_delta)}"
        return out

    def validate_move(self, board: Board) -> bool:
        """Validate the move against the board state.
        Args:
            board: Board state
        
        Returns:
            True if the move is valid, False otherwise
        """
        if self.building_card.card_type == 'none' and self.employee_delta == 0 and self.sell_price_delta == 0 and self.buy_price_delta == 0:
            return False # empty move
        if not self.validate_building_placement(board, self.building_coordinate[0], self.building_coordinate[1]):
            return False
        if not self.validate_employee_delta(board, self.employee_coordinate[0], self.employee_coordinate[1]):
            return False
        if not self.validate_sell_price_delta(board):
            return False
        if not self.validate_buy_price_delta(board):
            return False

        return True

    def validate_sell_price_delta(self, board: Board) -> bool:
        """Validate a change in sell price.
        
        Args:
            board: Board state
        """
        proposed_sell_price = board.player_sell_prices[self.player_ind] + self.sell_price_delta
        if proposed_sell_price in [2,3,4,5]:
            return True
        return False

    def validate_buy_price_delta(self, board: Board) -> bool:
        """Validate a change in buy price.
        
        Args:
            board: Board state
        """
        proposed_buy_price = board.player_buy_prices[self.player_ind] + self.buy_price_delta
        if proposed_buy_price in [1,2,3,4]:
            return True
        return False

    def validate_employee_delta(self, board: Board, row: int, col: int) -> bool:
        if self.employee_delta == 0:
            return True
        if board.mask[row][col] == 0:
            #print('invalid location for adding an employee')
            return False
        
        # check if player has building on location
        if board.player_bud_arrays[self.player_ind][row][col] == None or board.player_bud_arrays[self.player_ind][row][col].card_type == 'none':
            #print('no building on location')
            return False

        # count current emps
        board_card, curr_emps = board.card_array[row][col], 0
        for p in range(board.no_players):
            curr_emps += board.player_emp_arrays[p][row][col]

        if curr_emps + self.employee_delta >= board_card.max_employees:
            #print('no space for an additional emp')
            return False
        elif curr_emps + self.employee_delta < 0:
            #print('no emps to remove')
            return False
        else:
            return True

    def validate_building_placement(self, board: Board, row: int, col: int) -> bool:
        """Validate a building placement.
        
        Args:
            player_ind: Player index
            building_card: Building to add
            row: Row position
            col: Column position
        """

        # check if location is valid
        if board.mask[row][col] == 0:
            #print('invalid location for building card')
            return False

        # check if player has a building at this location already
        if board.player_bud_arrays[self.player_ind][row][col] != None and board.player_bud_arrays[self.player_ind][row][col].card_type != 'none':
            #print('player already has a building on this location')
            return False
        
        # check if building is allowed on board card
        board_card = board.card_array[row][col]
        if board_card.card_type not in self.building_card.allowed_board_cards:
            #print('invalid building card: ' + str(self.building_card.card_type) + ' | on board card: ' + str(board_card.card_type))
            return False
        
        # check if other player has a building on location
        p_count_on_location = 0
        for p in range(board.no_players):
            if board.player_bud_arrays[p][row][col] != None and board.player_bud_arrays[p][row][col].card_type != 'none':
                p_count_on_location += 1

        # check existing building card max players and that new card is correct type
        for p in range(board.no_players):
            if p != self.player_ind and board.player_bud_arrays[p][row][col] != None and board.player_bud_arrays[p][row][col].card_type != 'none':
                existing_bud_card = board.player_bud_arrays[p][row][col]
                if existing_bud_card.max_players == p_count_on_location:
                    #print('board card already has max players')
                    return False
                elif existing_bud_card.card_type != self.building_card.card_type:
                    #print('building needs to match existing building card type')
                    return False

        return True
    
    def apply(self, board: Board) -> Board:
        """Apply a move to the board.
        
        Args:
            board: Board
        """
        if self.building_card != None and self.building_card.card_type != 'none':
            board.player_bud_arrays[self.player_ind][self.building_coordinate[0]][self.building_coordinate[1]] = self.building_card
        
        if self.employee_delta != 0:
            board.player_emp_arrays[self.player_ind][self.employee_coordinate[0]][self.employee_coordinate[1]] += self.employee_delta
            
        if self.sell_price_delta != 0:
            board.player_sell_prices[self.player_ind] += self.sell_price_delta
            
        if self.buy_price_delta != 0:
            board.player_buy_prices[self.player_ind] += self.buy_price_delta
        return board