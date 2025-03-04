"""Game settings and configuration."""
from typing import Dict
from dataclasses import dataclass

@dataclass
class Settings:
    """Game settings configuration."""
    
    # Card properties
    base_emp_value: int = 1
    emp_cost: int = 1
    bud_cost: int = 1
    
    # Board size configuration
    no_players_to_board_size: Dict[int, int] = None
    
    # Card count configuration
    no_players_to_no_industry_cards: Dict[int, int] = None
    no_players_to_no_farm_cards: Dict[int, int] = None
    no_players_to_no_residential_cards: Dict[int, int] = None
    
    # Building placement rules
    hq_allowed_on: list = None
    buy_market_allowed_on: list = None
    sell_market_allowed_on: list = None
    process_allowed_on: list = None
    
    # Player settings
    player_starting_cap: int = 10
    no_of_turns_in_game: int = 12
    
    # Card names
    buy_card_name: str = 'Wheat Market'
    buy_process_card_name: str = 'Mill'
    sell_process_card_name: str = 'Bakery'
    sell_card_name: str = 'Bread Market'
    process_card_name: str = 'Factory'
    
    def __post_init__(self):
        """Initialize default values for dictionaries."""
        if self.no_players_to_board_size is None:
            self.no_players_to_board_size = {1:12, 2:16, 3:20, 4:24}
            
        if self.no_players_to_no_industry_cards is None:
            self.no_players_to_no_industry_cards = {1:4, 2:6, 3:8, 4:10}
            
        if self.no_players_to_no_farm_cards is None:
            self.no_players_to_no_farm_cards = {1:4, 2:5, 3:6, 4:7}
            
        if self.no_players_to_no_residential_cards is None:
            self.no_players_to_no_residential_cards = {1:4, 2:5, 3:6, 4:7}
            
        if self.hq_allowed_on is None:
            self.hq_allowed_on = ['industry', 'residential', 'farm']
            
        if self.buy_market_allowed_on is None:
            self.buy_market_allowed_on = ['farm']
            
        if self.sell_market_allowed_on is None:
            self.sell_market_allowed_on = ['residential']
            
        if self.process_allowed_on is None:
            self.process_allowed_on = ['industry']
