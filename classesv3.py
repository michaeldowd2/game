import random
import copy
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from os import listdir
from os.path import join
from matplotlib import patches
from pyfonts import load_font

ASSET_PATH = join('assets', 'theme_1')
IMG_IDX = {'demand':0, 'shop':0, 'product':0, 'unit_cost':0, 'unit_profit':0, 'employees_male':0, 'employees_female':0, 'sell_market':0, 'buy_market':0, 'process':0, 'hq':0}

class Card:
    def __init__(self, name, card_type = ''):
        self.name = name
        self.card_type = card_type
        if card_type == '':
            self.card_type = name.lower()

        self.image_path = ''
        if card_type != '' and card_type in IMG_IDX:
            path = join(ASSET_PATH, card_type)
            if os.path.exists(path):
                imgs = listdir(join(ASSET_PATH, card_type))
                img_idx = IMG_IDX[card_type]
                IMG_IDX[card_type] += 1
                self.image_path = join(ASSET_PATH, card_type, imgs[img_idx % len(imgs)])

class Deck:
    def __init__(self, cards):
        self.cards = cards
 
    def render(self):
        fig, axs = plt.subplots(1, len(self.cards))
        fig.set_figwidth(12)
        fig.set_figheight(3)
        
        for i, card in enumerate(self.cards):
            if card is not None:
                card.render(ax = axs[i])

    def remove_cards(self, cards):
        for card in cards:
            self.cards.remove(card)

    def take_N_random(self, N):
        res = []
        for i in range(N):
            x = random.choice(self.cards)
            self.cards.remove(x)
            res.append(x)
        return res

    def take_N_from_bottom(self, N):
        res = self.cards[0:N]
        self.employees = self.employees[N:]
        return res

    def take_N_from_top(self, N):
        res = self.cards[len(self.cards)-N:]
        self.cards = self.cards[0:len(self.cards)-N]
        return res

    def add_N_to_bottom(self, cards):
        self.cards = cards + self.cards
   
    def add_N_to_top(self, cards):
        self.cards = self.cards + cards       
    
    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards

class BuildingCard(Card):
    def __init__(self, name = '', card_type = '', x_name = '', y_name = '', max_output = 5, max_min = 2, max_players = 1, allowed_board_cards = []):
        super().__init__(name, card_type)
        valid_building_card_types = ['none','buy_market','sell_market','process','hq']
        if self.card_type not in valid_building_card_types:
            raise ValueError(f'Invalid card type: {self.card_type}')

        self.x_name = x_name
        self.y_name = y_name
        self.allowed_board_cards = allowed_board_cards
        self.max_players = max_players
        self.max_output = max_output

        self.max_min = max_min
        self.values, self.x_values, self.y_values = self.generate_values()
        self.title = self.name
        self.subtitle = 'Cost $1'

    def get_value(self, x, y):
        if x in self.x_values and y in self.y_values:
            return self.values[x][y]
        else:
            return 0
        if x not in self.x_values:
            if x < min(self.x_values):
                x = min(self.x_values)
            else:
                x = max(self.x_values)
        if y not in self.y_values:
            if y < min(self.y_values):
                y = min(self.y_values)
            else:
                y = max(self.y_values)
        return self.values[x][y]
    
    def generate_values(self):
        if self.card_type == 'buy_market':
            return self.generate_buy_market_values()
        elif self.card_type == 'sell_market':
            return self.generate_sell_market_values()
        elif self.card_type == 'process':
            return self.generate_process_values()
        else:
            return {}, [], []

    def generate_process_values(self):
        res = {
            0:{0:0,1:2,2:4},
            1:{0:2,1:4,2:6},
            2:{0:4,1:6,2:8}
        }
        return res, [0,1,2], [0,1,2]

    def generate_sell_market_values(self):
        res = {
            2:{2:6,4:4,5:5,6:6,7:7},
            3:{3:4,4:2,5:3,6:4,7:5,8:6},
            4:{4:2,5:1,6:2,7:3,8:4,9:5},
            5:{7:1,8:2,9:3,10:4}
        }
        return res, [2,3,4,5], [2,3,4,5,6,7,8,9,10]
    
    def generate_buy_market_values(self):
        res = {
            1:{1:5,2:4,3:3,4:2,5:1},
            2:{2:6,3:5,4:4,5:3,6:2},
            3:{3:7,4:6,5:5,6:4,7:3},
            4:{4:8,5:7,6:6,7:5,8:4}
        }
        return res, [1,2,3,4], [1,2,3,4,5,6,7,8]

    def render(self, ax = None, save_path = ''):
        def get_start_y_and_height(index):
            y_mod, h_mod, y_mods, h_mods = 0, 0, {0:0,1:2,2:8,3:4,4:2}, {0:2,1:6,2:-4,3:-2,4:-2} # modify start points and heights of rectangles
            if index in y_mods:
                y_mod = y_mods[index]
            if index in h_mods:
                h_mod = h_mods[index]
            return 113 * index + y_mod, 113 + h_mod
        def get_start_x_and_width(index):
            x_mod, w_mod, x_mods, w_mods = 0, 0, {0:0,1:0,2:-6,3:-10,4:0}, {0:0,1:-6,2:-4,3:10,4:0} # modify start points and widthsof rectangles
            if index in x_mods:
                x_mod = x_mods[index]
            if index in w_mods:
                w_mod = w_mods[index]
            return 113 * index + x_mod, 113 + w_mod

        fontsize1, y_axis_fontsize, fontsize3 = 8, 8, 12
        w, h, cell = 760, 760, 113
        y_axis_offset = -8
        
        font = load_font(font_url="https://github.com/google/fonts/blob/main/apache/specialelite/SpecialElite-Regular.ttf?raw=true")
        
        if ax == None:
            plt.figure(figsize=(w/100, h/100), dpi=100)
            ax = plt.gca()
    
        ax.set_xlim(0, w)
        ax.get_xaxis().set_ticks([])
        ax.set_ylim(0, h)
        ax.get_yaxis().set_ticks([])
    
        if self.image_path != '':
            img = plt.imread(self.image_path)
            imgplot = ax.imshow(img, extent=(0, w, 0, w))
        else:
            imgplot = ax.imshow(np.zeros((w, w)), extent=(0, w, 0, w))
           
        for i, x in enumerate(self.x_values):
            start_x, width = get_start_x_and_width(i)
            for j, y in enumerate(self.y_values):
                start_y, height = get_start_y_and_height(j)
                start_y = start_y + 195

                # y axis labels
                if i == 0:
                    lab = str(y)
                    ax.text(y_axis_offset, start_y + height / 2, lab, fontsize = y_axis_fontsize, ha = 'right', va = 'center', font = font)
                
                # x axis labels
                if j == len(self.y_values) - 1:
                    ax.text(start_x + width / 2, h + 8, str(x), fontsize = fontsize1, ha = 'center', va = 'bottom', font = font)
                
                # values
                value = self.get_value(x, y)
                if value != 0:
                    rect = patches.Rectangle((start_x, start_y), width, height, linewidth=1, edgecolor='black', facecolor='black', alpha = 0.2)
                    ax.add_patch(rect)
                    ax.text(start_x + width / 2, start_y + height / 2, str(value), fontsize = fontsize3, ha = 'center', va = 'center', color = 'white', font = font)
        
        ax.text(w, h + 8, self.x_name, fontsize = fontsize1, ha='right', va='bottom', font = font, rotation = 'horizontal')
        ax.text(y_axis_offset, 0, self.y_name, fontsize = y_axis_fontsize, ha='right', va='bottom', font = font, rotation = 'vertical')
       
        rect = patches.Rectangle((0, 0), w, 48, linewidth=1, edgecolor='black', facecolor='black', alpha = 0.4)
        ax.add_patch(rect)
        ax.text(16, 0, self.title, fontsize = fontsize1, ha = 'left', va = 'bottom', font = font, color = 'white')
        ax.text(w-16, 0, self.subtitle, fontsize = fontsize1, ha = 'right', va = 'bottom', font = font, color = 'white')

        if save_path != '':
            plt.savefig(save_path, dpi=100, bbox_inches='tight') 

    def str_render(self):
        print(self.name + ', max p: ' + str(self.max_players))
        for y in self.y_values[::-1]:
            y_str = str(y)
            if y <= 9:
                y_str += ' '
            for x in self.x_values:
                if x in self.values and y in self.values[x]:
                    y_str += ' | ' + str(self.values[x][y])
                else:
                    y_str += ' |  '
            y_str += ' |'
            print(y_str)
            ln_str = '   '
            for x in self.x_values:
                ln_str += '----'
            print(ln_str)
        x_str = '  '
        for x in self.x_values:
            x_str += '   ' + str(x)
        print(x_str)

    def __str__(self):
        if self.card_type == 'buy_market':
            return 'B'
        elif  self.card_type == 'sell_market':
            return 'S'
        elif self.card_type == 'process':
            return 'P'
        elif self.card_type == 'none':
            return '-'
        return ''
    
class BoardCard(Card):
    def __init__(self, name = '', card_type = '', max_employees = 3):
        super().__init__(name, card_type)
        self.max_employees = max_employees
    
    def __str__(self):
        if self.card_type == 'farm':
            return 'F' + str(self.max_employees)
        elif self.card_type == 'commerce':
            return 'C' + str(self.max_employees)
        elif self.card_type == 'industry':
            return 'I' + str(self.max_employees)
        elif self.card_type == 'residential':
            return 'R' + str(self.max_employees)
        return ''

class Settings:
    def __init__(self, 
                 base_emp_value = 1,
                 emp_cost = 1,
                 bud_cost = 1,
                 no_players_to_board_size = {1:12, 2:16, 3:20, 4:24},
                 no_players_to_no_industry_cards = {1:4, 2:6, 3:8, 4:10},
                 no_players_to_no_farm_cards = {1:4, 2:5, 3:6, 4:7},
                 no_players_to_no_residential_cards = {1:4, 2:5, 3:6, 4:7},
                 hq_allowed_on = ['industry', 'residential', 'farm'],
                 buy_market_allowed_on = ['farm'],
                 sell_market_allowed_on = ['residential'],
                 process_allowed_on = ['industry'],

                 player_starting_cap = 10,
                 no_of_turns_in_game = 12,
                 buy_card_name = 'Wheat Market',
                 buy_process_card_name = 'Mill',
                 sell_process_card_name = 'Bakery',
                 sell_card_name = 'Bread Market',
                 process_card_name = 'Factory'
            ):
        
        # card properties
        self.base_emp_value = base_emp_value
        self.emp_cost = emp_cost
        self.bud_cost = bud_cost

        # deck properties

        self.no_players_to_board_size = no_players_to_board_size

        self.no_players_to_no_industry_cards = no_players_to_no_industry_cards
        self.no_players_to_no_farm_cards = no_players_to_no_farm_cards
        self.no_players_to_no_residential_cards = no_players_to_no_residential_cards

        self.hq_allowed_on = hq_allowed_on
        self.buy_market_allowed_on = buy_market_allowed_on
        self.sell_market_allowed_on = sell_market_allowed_on
        self.process_allowed_on = process_allowed_on

        # player properties
        self.player_starting_cap = player_starting_cap
        self.no_of_turns_in_game = no_of_turns_in_game

        # game names
        self.buy_card_name = buy_card_name
        self.buy_process_card_name = buy_process_card_name
        self.sell_process_card_name = sell_process_card_name
        self.sell_card_name = sell_card_name
        self.process_card_name = process_card_name

class Player:
    def __init__(self, game_settings):
        self.game_settings = game_settings

    def find_move(self, player_no,company, available_employees, available_buildings, market_strength, other_players_des = -1, debug = 0):
        test_emp_idx_combos = self.generate_move_combinations(len(available_employees)) # hire up to two employees per turn
        test_bud_idxs = [-1] + list(range(len(available_buildings))) # pick up to one building per turn
        test_prices = list(self.game_settings.price_to_price_des.keys())
        
        best_net, best_emp_combo, best_bud_idx, best_price = -10000, [], -1, 5
        #if player_no == 1:
        #    print('here')
        for test_emp_idx_combo in test_emp_idx_combos:
            test_emps = copy.deepcopy(company.employees)
            for test_emp_idx in test_emp_idx_combo:
                test_emps.append(available_employees[test_emp_idx])
            
            for bud_idx in test_bud_idxs:
                test_buds = copy.deepcopy(company.buildings)
                if bud_idx != -1:
                    test_buds.append(available_buildings[bud_idx])
            
                for test_price in test_prices:
                    valid, test_des = company.calculate_desirability(test_emps, test_price, debug)
                    if valid:
                        total_des = test_des + other_players_des
                        valid, test_net = company.calculate_net(test_emps, test_buds, test_price, market_strength, total_des, debug)
                        if valid:
                            if test_net > best_net:
                                best_net = test_net
                                best_emp_combo = test_emp_idx_combo
                                best_bud_idx = bud_idx
                                best_price = test_price
                                if debug > 1:
                                    print('new best set, best possible net: ' + str(best_net) + ', best emp combo: ' + str(best_emp_combo) + ', best bud idx: ' + str(best_bud_idx) + ', best price: ' + str(best_price))
        if debug:
            print('new best set, best possible net: ' + str(best_net) + ', best emp combo: ' + str(best_emp_combo) + ', best bud idx: ' + str(best_bud_idx) + ', best price: ' + str(best_price))
        return best_emp_combo, best_bud_idx, best_price, best_net

    def generate_move_combinations(self, available_cards, max_combos = 2 ):
        res = []
        for i in range(available_cards):
            res.append([i])
            for j in range(i, available_cards):
                if i != j:
                    res.append([i,j])
        return res
    
    def generate_and_analyse_game_states(self, market_strength = -1, iterations = 100, debug = 0):
        desks_per_office = self.game_settings.office_to_desk

        ops_emp_ls = list(self.game_settings.operations_to_max_buildings.keys())
        all_fin_emps = list(self.game_settings.finance_to_max_gross.keys())
        all_eng_emps = list(self.game_settings.engineering_to_unit_cost.keys())
        all_mkt_emps = list(self.game_settings.marketing_to_brand.keys())

        x, y, res = 0, 0, []
        # set up lists for each attribute
        mkt_str, gs_keys, ops_ls, fin_ls, eng_ls, mkt_ls, off_ls, fac_ls, prc_ls, cst_ls, net_ls = [], [], [], [], [], [], [], [], [], [], []
        while x < iterations and y < 50000:
            ops_emp, eng_emp, fin_emp, mkt_emp = 0, 0, 0, 0

            ops_emp = random.choice(ops_emp_ls) # choose random number of ops employees
            max_buildings = self.game_settings.operations_to_max_buildings[ops_emp] # get max buildings based on ops employees
            min_offices = math.ceil(ops_emp / desks_per_office) # get min required offices based on ops employees

            # pick random combinations of buildings that are allowed
            no_off = random.randint(min_offices, max_buildings)
            no_fac = random.randint(0, max_buildings - no_off)

            # pick random remaining employees
            max_remaining_emp = no_off * desks_per_office * self.game_settings.base_emp_value - ops_emp
            if max_remaining_emp > 0:
                allowed_eng_emps = [x for x in all_eng_emps if x <= max_remaining_emp]
                eng_emp = random.choice(allowed_eng_emps)
                max_remaining_emp = max_remaining_emp - eng_emp
                if max_remaining_emp > 0:
                    allowed_fin_emps = [x for x in all_fin_emps if x <= max_remaining_emp]
                    fin_emp = random.choice(allowed_fin_emps)
                    max_remaining_emp = max_remaining_emp - fin_emp
                    if max_remaining_emp > 0:
                        allowed_mkt_emps = [x for x in all_mkt_emps if x <= max_remaining_emp]
                        mkt_emp = random.choice(allowed_mkt_emps)

            # pick random price between cost and max price
            unit_cost = self.game_settings.engineering_to_unit_cost[eng_emp]
            pos_prc_ls = list(self.game_settings.price_to_price_des.keys())
            pos_prc_ls = [x for x in pos_prc_ls if x > unit_cost]
            if pos_prc_ls == [] or pos_prc_ls == None:
                continue # if unit cost = price this isn't worth considering
            sel_prc = random.choice(pos_prc_ls)
            
            key = [ops_emp, fin_emp, eng_emp, mkt_emp, no_off, no_fac, sel_prc]
            key = tuple(key)
            # build player hand from random combinations
            if key not in res:
                mkt_str.append(market_strength)
                gs_keys.append(key)
                ops_ls.append(ops_emp)
                fin_ls.append(fin_emp)
                eng_ls.append(eng_emp)
                mkt_ls.append(mkt_emp)
                off_ls.append(no_off)
                fac_ls.append(no_fac)
                prc_ls.append(sel_prc)
                cst_ls.append(unit_cost)
                net = self.company.analyse_game_state(key, market_strength, debug = debug)
                net_ls.append(net[1])
                res.append(key)
                x += 1
            else:
                if debug > 1:
                    print('iteration: ' + str(x) + ', existing net for key: ' + str(key))
            y += 1
        
        # create pandas dataframe
        df = pd.DataFrame({'market strength':mkt_str,
                           'gamestate key':gs_keys,
                           'operations':ops_ls,
                           'finance':fin_ls,
                           'engineering':eng_ls,
                           'marketing':mkt_ls,
                           'offices':off_ls,
                           'factories':fac_ls,
                           'price':prc_ls,
                           'unit cost (derived)':cst_ls,
                           'net income':net_ls})
        
        return df

class Board:
    def __init__(self, game_settings, no_players, shuffle = True, style = 'rectangle'):
        self.game_settings = game_settings
        self.no_players = no_players
        self.style = style

        self.size = game_settings.no_players_to_board_size[no_players]
        self.cards = self.gen_all_board_cards(game_settings, no_players, shuffle)
        if self.size != len(self.cards):
            raise Exception('Board Error: board size does not match number of cards')
        
        self.mask = self.gen_mask(self.size, style)
        self.location_to_card_index, self.card_index_to_location = self.gen_board_indices(self.mask)
        self.card_array = self.gen_card_array(self.mask, self.location_to_card_index, self.cards)
        
        self.player_bud_arrays, self.player_emp_arrays = self.gen_player_arrays(no_players, self.mask)
        self.player_buy_prices, self.player_sell_prices = [1] * no_players, [2] * no_players
        
    def __str__(self):
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
    
    def render(self):
        fig, axs = plt.subplots(self.board_size, self.board_size)
        fig.set_figwidth(3.5 * self.board_size)
        fig.set_figheight(3.5 * self.board_size)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].render(ax = axs[i][j])

    def gen_all_board_cards(self, game_settings, no_players, shuffle = True):
        # board cards
        no_farm_cards = game_settings.no_players_to_no_farm_cards[no_players]
        no_residential_cards = game_settings.no_players_to_no_residential_cards[no_players]
        no_industry_cards = game_settings.no_players_to_no_industry_cards[no_players]
        farm_cards = self.gen_board_cards(no_farm_cards, 'Farm', 'farm', 4)
        residential_cards = self.gen_board_cards(no_residential_cards, 'Residential', 'residential', 4)
        industry_cards = self.gen_board_cards(no_industry_cards, 'Industry', 'industry', 4)
        board_cards = farm_cards + residential_cards + industry_cards
        if shuffle:
            board_cards = Deck(board_cards).shuffle()

        return board_cards

    def gen_board_cards(self, count, name, card_type, max_employees):
        cards = []
        for i in range(count):
            cards.append(BoardCard(name = name, card_type = card_type, max_employees = max_employees))
        return cards
 
    def gen_mask(self, size, style):
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

    def gen_board_indices(self, board_array):
        location_to_card_index, card_index_to_location, card_index = {}, {}, 0
        for r in range(len(board_array)):
            for c in range(len(board_array[0])):
                if board_array[r][c] == 1:
                    card_index_to_location[card_index] = (r,c)
                    location_to_card_index[(r,c)] = card_index
                    card_index += 1
        return location_to_card_index, card_index_to_location

    def gen_card_array(self, mask, location_to_card_index, cards):
        card_array = np.zeros((len(mask), len(mask[0]))).tolist()
        for r in range(len(mask)):
            for c in range(len(mask[0])):
                if mask[r][c] == 1:
                    card_array[r][c] = cards[location_to_card_index[(r,c)]]
                else:
                    card_array[r][c] = None
        return card_array

    def gen_player_arrays(self, no_players, board_array):
        player_bud_arrays, player_emp_arrays = [], []
        for p in range(no_players):
            #create an array for each player the same size as the board
            bud_arr = np.zeros((len(board_array), len(board_array[0]))).tolist()
            emp_arr = np.zeros((len(board_array), len(board_array[0]))).tolist()

            for i in range(len(board_array)):
                for j in range(len(board_array[0])):
                    bud_arr[i][j], emp_arr[i][j] = None, None
                    if board_array[i][j] == 1:
                        bud_arr[i][j], emp_arr[i][j] = BuildingCard('None', 'none', max_players=4), 0
            player_bud_arrays.append(bud_arr)
            player_emp_arrays.append(emp_arr)

        return player_bud_arrays, player_emp_arrays

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
        
    def add_building(self, player_ind, building_card, row, col):
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
        
        self.player_bud_arrays[player_ind][row][col] = building_card
        return True
        
    def add_employee(self, player_ind, row, col):
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

        if curr_emps >= board_card.max_employees:
            print('no space for an additional emp')
            return False
        else:
            self.player_emp_arrays[player_ind][row][col] += 1

    def change_buy_price(self, player_ind, price):
        # check price is valid
        if price not in [1,2,3,4]:
            print('invalid buy price')
            return False
        self.player_buy_prices[player_ind] = price
        return True
    
    def change_sell_price(self, player_ind, price):
        # check price is valid
        if price not in [2,3,4,5]:
            print('invalid sell price')
            return False
        self.player_sell_prices[player_ind] = price
        return True
    
class Game:
    def __init__(self, game_settings, no_players, board_style = 'rectangle',theme = 'theme_0', shuffle = True, debug = 0):
        self.asset_path = join('assets', theme)
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings
        self.turn_number = 0

        # building cards - this is a deck that will be taken from arbitrarily
        buy_market_cards = self.gen_building_cards(100, game_settings.buy_card_name, 'buy_market', game_settings.buy_market_allowed_on, 'Total Spend', 'Player Spend', 2, 5)
        sell_market_cards = self.gen_building_cards(100, game_settings.sell_card_name, 'sell_market', game_settings.sell_market_allowed_on, 'Total Price', 'Player Price', 2, 5)
        process_cards = self.gen_building_cards(100, game_settings.process_card_name, 'process', game_settings.process_allowed_on, 'Connected ' + game_settings.buy_card_name, 'Connected ' + game_settings.sell_card_name, 1, 10)
        hq_cards = self.gen_building_cards(100, 'HQ', 'hq', game_settings.hq_allowed_on, 'Max Buildings', 'Max Employees', 1, 5)
        
        self.building_cards = {
            'buy_market': buy_market_cards,
            'sell_market': sell_market_cards,
            'process': process_cards,
            'hq': hq_cards
        }

        # board
        self.board = Board(game_settings, no_players, shuffle, board_style)
        
        # players
        self.players = [Player(game_settings) for i in range(no_players)]

    def run_turn(self, render = False, debug = 0):
        player_desirabilities, player_current_nets, new_player_desirabilities = [], [], []
        prev_market_val, new_market_val = self.market.current_strength, self.market.current_strength

        # this will force a the next player to go first each turn and loop around
        players, ordered_players = list(range(self.no_players)), []
        for i in range(self.turn_number, len(players) + self.turn_number):
            ordered_players.append(players[i % len(players)])

        if debug:
            print('TURN ' + str(self.turn_number))
            
        # Draw cards for turn
        building_pool = self.building_deck.take_N_from_top(self.game_settings.no_bud_cards_in_pool)

        if debug:
            building_pool_str, employee_pool_str = '-- BUD Pool | ', '-- EMP Pool | '
            i = 0
            for b in building_pool:
                building_pool_str += 'B' + str(i) + ' ' +str(b) + ' | '
                i += 1
            print(building_pool_str + '\n' + employee_pool_str)

        if render:
            self.render_current_turn_cards(market_card, building_pool)

        # calc current desirability
        for p in ordered_players: #range(self.no_players):
            is_valid, current_p_des = self.companies[p].calculate_desirability(self.companies[p].employees, self.companies[p].current_price)
            player_desirabilities.append(current_p_des)
        
        # calc current net income
        for p in ordered_players:
            total_desirability = sum(player_desirabilities)
            current_hand_dic = self.companies[p].get_hand_dic()
            is_valid, current_p_net = self.companies[p].calculate_net(self.companies[p].employees, self.companies[p].buildings, self.companies[p].current_price, self.market.current_strength, total_desirability, max([0, debug-1]))
            
            if debug:
                print('-- P' + str(p) + ', start hand: ' + str(current_hand_dic) + ', cur des: ' + str(current_p_des) + ', tot des:' +  str(total_desirability) + ', cur net: ' + str(current_p_net))
                
            player_current_nets.append(current_p_net)
        
        # find move
        for p in ordered_players: #range(self.no_players):
            player = self.players[p]
            company = self.companies[p]
            other_player_des = total_desirability - player_desirabilities[p]
            best_emp_combo, best_bud_idx, best_price, best_net = player.find_move(p, company, employee_pool, building_pool, self.market.current_strength, other_players_des = other_player_des, debug = 0)
            
            # hire employee into hand
            emps = []
            for ind in best_emp_combo:
                emps.append(employee_pool[ind])
            for emp in emps:
                company.hire_employee(emp)
                employee_pool.remove(emp) # remove them from the pool
            # hire building into hand
            if best_bud_idx != -1:
                bud = building_pool[best_bud_idx]
                company.rent_building(bud)
                building_pool.remove(bud) # remove them from the pool
            # update current price
            company.current_price = best_price
            
            valid, test_des = company.calculate_desirability(company.employees, best_price, debug)
            new_player_desirabilities.append(test_des)

            if debug:
                is_valid, best_net = company.calculate_net(company.employees, company.buildings, best_price, self.market.current_strength, other_player_des+test_des, max([0, debug-1]))
                new_hand_dic = self.companies[p].get_hand_dic()
                print('-- P' + str(p) + ', best move: pick employees: ' + str(best_emp_combo) + ', pick building: ' + str(best_bud_idx) + ', set price: ' + str(best_price))
                print('-- P' + str(p) + ', final hand: ' + str(new_hand_dic) + ', new des: ' + str(test_des) + ', tot des:' +  str(other_player_des+test_des) + ', targ net: ' + str(best_net))
                
        # calculate final demands and net income
        final_total_desirability = sum(new_player_desirabilities)
        for p in ordered_players: #range(self.no_players):
            company = self.companies[p]
            valid, final_p_net = company.calculate_net(company.employees, company.buildings, company.current_price, self.market.current_strength, final_total_desirability, max([0, debug-1]))
            player_current_nets[p] = final_p_net
            if debug:
                print('-- P' + str(p) + ', fin des: ' + str(new_player_desirabilities[p]) + ', tot des:' +  str(final_total_desirability) + ', fin net: ' + str(final_p_net))

        if render:
            self.market.render(player_desirabilities = player_desirabilities)
        
        # Add cards back into decks
        self.market_deck.add_N_to_bottom([market_card])
        self.building_deck.add_N_to_bottom(building_pool)
        self.employee_deck.add_N_to_bottom(employee_pool)

        if debug:
            print()
        self.turn_number += 1
        
    def gen_building_cards(self, count, name, card_type, allowed_on, x_name, y_name, max_players, max_output):
        cards = []
        for i in range(count):
            cards.append(BuildingCard(name = name, card_type = card_type, x_name = x_name, y_name = y_name, max_players = max_players, max_output = max_output, allowed_board_cards = allowed_on))
        return cards

    def render_current_turn_cards(self, bud_cards):
        self.render_row_of_cards(['Building Card Pool'], bud_cards)

    def render_row_of_cards(self, titles, cards):
        fig, axs = plt.subplots(1, len(cards))
        fig.set_figwidth(15)
        for i, card in enumerate(cards):
            if len(titles) > 0 and i == 0:
                axs[i].set_title(titles[0], loc='left')
            if len(titles) > 1 and i == len(cards) - 1:
                axs[i].set_title(titles[1], loc='right')
            if card is None:
                self.render_none(axs[i])
            else:
                
                card.render(ax = axs[i])
    
    def render_none(self, ax = None):
        props = {'w':256, 'h':339, 'p':6, 'r':24, 'fs1': 9, 'fs2': 10, 'fs3': 8}
        w, h, p, r = props['w'], props['h'], props['p'], props['r']
        
        if ax == None:
            plt.figure(figsize=(w/100, h/100), dpi=100)
            ax = plt.gca()
        
        ax.set_xlim(0, w)
        ax.set_ylim(0, h)
        # disable axis outlines and ticks
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
