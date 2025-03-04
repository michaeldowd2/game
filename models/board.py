"""Board model for game state."""
from typing import List, Dict, Tuple, Optional
import random
import numpy as np
from .settings import Settings
from .board_card import BoardCard
from .building_card import BuildingCard

class Board:
    """Represents the game board and manages its state."""
    
    def __init__(self, game_settings: Settings, no_players: int, shuffle: bool = True, style: str = 'rectangle'):
        """Initialize the game board.
        
        Args:
            game_settings: Game settings configuration
            no_players: Number of players
            shuffle: Whether to shuffle board cards
            style: Board layout style ('rectangle' or other)
        """
        self.game_settings = game_settings
        self.no_players = no_players
        self.style = style

        self.size = game_settings.no_players_to_board_size[no_players]
        self.cards = self.gen_all_board_cards(game_settings, no_players, shuffle)
        if self.size != len(self.cards):
            raise ValueError('Board Error: board size does not match number of cards')
        
        self.mask = self.gen_mask(self.size, style)
        self.location_to_card_index, self.card_index_to_location = self.gen_board_indices(self.mask)
        self.card_array = self.gen_card_array(self.mask, self.location_to_card_index, self.cards)
        
        self.player_bud_arrays, self.player_emp_arrays = self.gen_player_arrays(no_players, self.mask)
        self.player_buy_prices, self.player_sell_prices = [1] * no_players, [2] * no_players

    def __str__(self) -> str:
        """String representation of the board.
        
        Returns:
            Formatted string showing board state
        """
        s = ''
        for r in range(len(self.mask)):
            s2 = ''
            for c in range(len(self.mask[0])):
                card_str = '| '
                if self.mask[r][c] == 1:
                    card_index = self.location_to_card_index[(r,c)]
                    card_str += str(self.cards[card_index])
                    for p in range(self.no_players):
                        card_str += ' ' + str(self.player_bud_arrays[p][r][c])
                        card_str += str(self.player_emp_arrays[p][r][c])
                else:
                    card_str += '  '
                    for p in range(self.no_players):
                        card_str += '   '
                card_str += ' |'
                s2 += card_str
            
            s += s2 + '\n'
            s = s.replace('||', '|').replace('  |  ', '     ')
        return s

    def gen_all_board_cards(self, game_settings: Settings, no_players: int,
                          shuffle: bool = True) -> List[BoardCard]:
        """Generate all board cards for the game.
        
        Args:
            game_settings: Game settings
            no_players: Number of players
            shuffle: Whether to shuffle cards
            
        Returns:
            List of generated board cards
        """
        cards = []
        cards.extend(self.gen_board_cards(
            game_settings.no_players_to_no_industry_cards[no_players],
            'Industry', 'industry', 3))
        cards.extend(self.gen_board_cards(
            game_settings.no_players_to_no_farm_cards[no_players],
            'Farm', 'farm', 3))
        cards.extend(self.gen_board_cards(
            game_settings.no_players_to_no_residential_cards[no_players],
            'Residential', 'residential', 3))
        
        if shuffle:
            random.shuffle(cards)
        return cards

    def gen_board_cards(self, count: int, name: str, card_type: str,
                       max_employees: int) -> List[BoardCard]:
        """Generate a specific type of board cards.
        
        Args:
            count: Number of cards to generate
            name: Name for the cards
            card_type: Type of cards
            max_employees: Maximum employees per card
            
        Returns:
            List of generated cards
        """
        return [BoardCard(name, card_type, max_employees) for _ in range(count)]

    def gen_mask(self, size: int, style: str) -> List[List[int]]:
        """Generate board mask based on style.
        
        Args:
            size: Board size
            style: Board layout style
            
        Returns:
            2D list representing board mask
        """
        if size not in [12,16,20,24,28,32,36]:
            raise Exception('board size not supported')
        if style not in  ['rectangle','diamond','linear']:
            raise Exception('board style not supported')
        
        row_c, col_c, row_not_in, col_not_in = 0, 0, [], []
        if size == 12:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 4, 3, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 4, 4, [0,3], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 4, 4, [1,2,3], [1,2]
        elif size == 16:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 4, 4, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 5, 4, [0,4], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 6, 4, [1,2,3,4], [1,2]
        elif size == 20:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 5, 4, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 7, 4, [0,1,5,6], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 8, 4, [1,2,3,4,5,6], [1,2]
        elif size == 24:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 6, 4, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 7, 4, [0,6], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 10, 4, [1,2,3,4,5,6,7,8], [1,2]
        elif size == 28:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 7, 4, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 8, 4, [0,7], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 12, 4, [1,2,3,4,5,6,7,8,9,10], [1,2]
        elif size == 32:
            if style == 'rectangle':
                row_c, col_c, row_not_in, col_not_in = 8, 4, [], []
            elif style == 'diamond':
                row_c, col_c, row_not_in, col_not_in = 9, 4, [0,8], [0,3]
            elif style == 'linear':
                row_c, col_c, row_not_in, col_not_in = 14, 4, [1,2,3,4,5,6,7,8,9,10,11,12], [1,2]
        
        rows = []
        for r in range(row_c):
            row = []
            for c in range(col_c):
                if r not in row_not_in or c not in col_not_in:
                    row.append(1)
                else:
                    row.append(0)
            rows.append(row)
        return rows

    def gen_board_indices(self, board_array: List[List[int]]) -> Tuple[Dict[Tuple[int, int], int], Dict[int, Tuple[int, int]]]:
        """Generate mappings between board locations and card indices.
        
        Args:
            board_array: 2D board array
            
        Returns:
            Tuple of dictionaries mapping locations to indices and vice versa
        """
        location_to_card_index = {}
        card_index_to_location = {}
        card_index = 0
        
        for i in range(len(board_array)):
            for j in range(len(board_array[0])):
                if board_array[i][j] == 1:
                    location_to_card_index[(i,j)] = card_index
                    card_index_to_location[card_index] = (i,j)
                    card_index += 1
                    
        return location_to_card_index, card_index_to_location

    def gen_card_array(self, mask: List[List[int]], location_to_card_index: Dict[Tuple[int, int], int],
                      cards: List[BoardCard]) -> List[List[Optional[BoardCard]]]:
        """Generate 2D array of cards based on mask.
        
        Args:
            mask: Board mask
            location_to_card_index: Mapping of locations to card indices
            cards: List of board cards
            
        Returns:
            2D array of cards
        """
        card_array = [[None for _ in range(len(mask[0]))] for _ in range(len(mask))]
        for i in range(len(mask)):
            for j in range(len(mask[0])):
                if mask[i][j] == 1:
                    card_array[i][j] = cards[location_to_card_index[(i,j)]]
        return card_array

    def gen_player_arrays(self, no_players: int, board_array: List[List[int]]) -> Tuple[List[List[List]], List[List[List[int]]]]:
        """Generate arrays tracking player buildings and employees.
        
        Args:
            no_players: Number of players
            board_array: Board layout array
            
        Returns:
            Tuple of arrays for buildings and employees
        """
        height, width = len(board_array), len(board_array[0])
        bud_arrays = [[[BuildingCard('None', 'none', max_players=4) for _ in range(width)] for _ in range(height)] for _ in range(no_players)]
        emp_arrays = [[[0 for _ in range(width)] for _ in range(height)] for _ in range(no_players)]
        return bud_arrays, emp_arrays

    def calc_player_net(self, player_ind):
        sum_buy, sum_process, sum_sell, tot_buds, tot_emps = 0, 0, 0, 0, 0
        player_buy_price = self.player_buy_prices[player_ind]
        player_sell_price = self.player_sell_prices[player_ind]

        for ind in self.card_index_to_location:
            i = self.card_index_to_location[ind][0]
            j = self.card_index_to_location[ind][1]
            card = self.player_bud_arrays[player_ind][i][j]
            tot_price = 0

            # player emps on current card
            curr_emp = self.player_emp_arrays[player_ind][i][j]
            tot_emps += curr_emp
            if card.card_type in ['buy_market','sell_market','process','hq']:
                tot_buds += 1
            
            if card.card_type == 'buy_market':
                for p in range(self.no_players):
                    if self.player_bud_arrays[p][i][j].card_type == 'buy_market':
                        tot_price += self.player_buy_prices[p]
                sum_buy += card.get_value(player_buy_price, tot_price) + curr_emp
            elif card.card_type == 'sell_market':
                for p in range(self.no_players):
                    if self.player_bud_arrays[p][i][j].card_type == 'sell_market':
                        tot_price += self.player_sell_prices[p]
                sum_sell += card.get_value(player_sell_price, tot_price) + curr_emp
            elif card.card_type == 'process':
                connected_buy_cards, connected_sell_cards = 0, 0
                connected_inds = [(i-1,j),(i,j+1),(i+1,j),(i,j-1)]
                for conn_ind in connected_inds:
                    ii, jj = conn_ind[0], conn_ind[1]
                    if ii >= 0 and jj >= 0 and ii < len(self.mask) and jj < len(self.mask[0]):
                        if self.player_bud_arrays[player_ind][ii][jj] != None:
                            if self.player_bud_arrays[player_ind][ii][jj].card_type == 'buy_market':
                                connected_buy_cards += 1
                            elif self.player_bud_arrays[player_ind][ii][jj].card_type == 'sell_market':
                                connected_sell_cards += 1
                sum_process += card.get_value(connected_buy_cards, connected_sell_cards) + curr_emp
            elif card.card_type == 'hq':
                pass        
            elif card.card_type == 'none':
                pass
        units = min(sum_buy, sum_process, sum_sell)
        net = units * (player_sell_price - player_buy_price) - tot_buds - tot_emps

        print('sum buy: ' + str(sum_buy) + ' | sum process: ' + str(sum_process) + ' | sum sell: ' + str(sum_sell))
        print('tot buds: ' + str(tot_buds) + ' | tot emps: ' + str(tot_emps) + ' | tot cost: ' + str(tot_buds + tot_emps))
        print('units: ' + str(units) + ' | player sell price: ' + str(player_sell_price) + ' | player buy price: ' + str(player_buy_price) + ' | net: ' + str(net))

        return net

    def add_building(self, player_ind: int, building_card: BuildingCard, row: int, col: int) -> bool:
        """Add a building to the board.
        Args:
            player_ind: Player index
            building_card: Building to add
            row: Row position
            col: Column position
        """
        if self.validate_building_placement(player_ind, building_card, row, col) == False:
            return False
        
        self.player_bud_arrays[player_ind][row][col] = building_card
        return True
    
    def validate_building_placement(self, player_ind: int, building_card: BuildingCard, row: int, col: int) -> bool:
        """Validate a building placement.
        
        Args:
            player_ind: Player index
            building_card: Building to add
            row: Row position
            col: Column position
        """

        # check if location is valid
        if self.mask[row][col] == 0:
            print('invalid location for building card')
            return False
        
        # check if building is allowed on board card
        board_card = self.card_array[row][col]
        if board_card.card_type not in building_card.allowed_board_cards:
            print('invalid building card: ' + str(building_card.card_type) + ' | on board card: ' + str(board_card.card_type))
            return False
        
        # check if other player has a building on location
        p_count_on_location = 0
        for p in range(self.no_players):
            if self.player_bud_arrays[p][row][col] != None and self.player_bud_arrays[p][row][col].card_type != 'none':
                p_count_on_location += 1

        # check existing building card max players and that new card is correct type
        for p in range(self.no_players):
            if p != player_ind and self.player_bud_arrays[p][row][col] != None and self.player_bud_arrays[p][row][col].card_type != 'none':
                existing_bud_card = self.player_bud_arrays[p][row][col]
                if existing_bud_card.max_players == p_count_on_location:
                    print('board card already has max players')
                    return False
                elif existing_bud_card.card_type != building_card.card_type:
                    print('building needs to match existing building card type')
                    return False

        return True

    def change_employee(self, player_ind: int, delta: int, row: int, col: int) -> None:
        """Add an employee to a position.
        
        Args:
            player_ind: Player index
            delta: Number of employees to add
            row: Row position
            col: Column position
        """
        if self.validate_employee_delta(player_ind, delta, row, col) == False:
            return False
        self.player_emp_arrays[player_ind][row][col] += delta

    def validate_employee_delta(self, player_ind, delta, row, col):
        if self.mask[row][col] == 0:
            print('invalid location for adding an employee')
            return False
        
        # check if player has building on location
        if self.player_bud_arrays[player_ind][row][col] == None or self.player_bud_arrays[player_ind][row][col].card_type == 'none':
            print('no building on location')
            return False

        # count current emps
        board_card, curr_emps = self.card_array[row][col], 0
        for p in range(self.no_players):
            curr_emps += self.player_emp_arrays[p][row][col]

        if curr_emps + delta >= board_card.max_employees:
            print('no space for an additional emp')
            return False
        elif curr_emps + delta < 0:
            print('no emps to remove')
            return False
        else:
            self.player_emp_arrays[player_ind][row][col] += delta

    def change_buy_price(self, player_ind: int, delta: int) -> None:
        """Change a player's buy price.
        
        Args:
            player_ind: Player index
            delta: Change in buy price
        """
        if not self.validate_buy_price_delta(player_ind, delta):
            return False
        self.player_buy_prices[player_ind] += delta

    def validate_buy_price_delta(self, player_ind: int, delta: int) -> bool:
        """Validate a change in buy price.
        
        Args:
            player_ind: Player index
            delta: change in buy price
        """
        proposed_buy_price = self.player_buy_prices[player_ind] + delta
        if proposed_buy_price in [1,2,3,4]:
            return True
        return False

    def change_sell_price(self, player_ind: int, delta: int) -> None:
        """Change a player's sell price.
        
        Args:
            player_ind: Player index
            delta: change in sell price
        """
        if not self.validate_sell_price_delta(player_ind, delta):
            return False
        self.player_sell_prices[player_ind] += delta
        return True
    
    def validate_sell_price_delta(self, player_ind: int, delta: int) -> bool:
        """Validate a change in sell price.
        
        Args:
            player_ind: Player index
            delta: New price
        """
        proposed_sell_price = self.player_sell_prices[player_ind] + delta
        if proposed_sell_price in [2,3,4,5]:
            return True
        return False
