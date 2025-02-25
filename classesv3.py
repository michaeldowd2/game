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
IMG_IDX = {'demand':0, 'shop':0, 'product':0, 'unit_cost':0, 'unit_profit':0, 'employees_male':0, 'employees_female':0, 'sales_district':0, 'material_district':0, 'production_district':0}

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
    def __init__(self, name = '', card_type = '', x_name = '', y_name = '', x_values = [], y_values = [], max_output = 5, max_min = 2, max_players = 1):
        super().__init__(name, card_type)
        self.x_name = x_name
        self.y_name = y_name
        self.x_values = x_values
        self.y_values = y_values

        self.max_output = max_output
        self.max_min = max_min
        self.values = self.generate_values()
        self.title = self.generate_title()
        self.subtitle = 'Cost $1'

    def get_value(self, x, y):
        if x in self.x_values and y in self.y_values:
            return self.values[x][y]
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
        res, max_price = {}, max(self.y_values)
        for x in self.x_values:
            x_res = {}
            for y in self.y_values:
                min_row_min, max_row_max = min(self.x_values), max(self.x_values)
                y_ratio = (y-1) / (max(self.y_values)-1)
                x_ratio = (x-1) / (max(self.x_values)-1)
                row_min = self.lerp(min_row_min, self.max_min, y_ratio)
                row_max = self.lerp(self.max_min, max_row_max, y_ratio)
                value = self.lerp(row_min, row_max, x_ratio)
                x_res[y] = int(value)
            res[x] = x_res
        return res

    def lerp(self, row_min, row_max, ratio):
        return (row_max - row_min) * ratio + row_min 
    
    def generate_title(self):
        return self.name

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

    def __str__(self):
        if self.card_type == 'buy_card':
            return 'BM'
        elif  self.card_type == 'sell_card':
            return 'SM'
        elif  self.card_type == 'buy_process_card':
            return 'BP'
        elif  self.card_type == 'sell_process_card':
            return 'SP'
        return ''
    
class BoardCard(Card):
    def __init__(self, name = '', card_type = '', max_emps = 3):
        super().__init__(name, card_type)
        self.max_emps = max_emps
    
    def __str__(self):
        if self.card_type == 'farm':
            return 'F' + str(self.max_emps)
        elif self.card_type == 'commerce':
            return 'C' + str(self.max_emps)
        elif self.card_type == 'industry':
            return 'I' + str(self.max_emps)
        elif self.card_type == 'residential':
            return 'R' + str(self.max_emps)
        return ''

class Company:
    def __init__(self, game_settings, market):
        self.game_settings = game_settings
        self.market = market
        self.employees = []
        self.buildings = []
        self.current_price = 5
        self.capital = game_settings.player_starting_cap
        
        # mapping cards
        #prices, markets = [4,5,6,7,8], [1,2,3,4,5]
        #self.product_mapping = MappingCard(name = 'Product', x_name = 'Brand', y_name = 'Price', x_values = [1,2,3,4,5], y_values = prices, type = 'product', max_output = 5)
        #self.demand_mapping = MappingCard(name = 'Demand: P', x_name = 'Product', y_name = 'Market', x_values = [1,2,3,4,5], y_values = markets, type = 'demand', max_output = 5)
        #self.unit_cost_mapping = MappingCard(name = 'Unit Cost', x_name = 'Ops', y_name = 'Market', x_values = [1,2,3,4,5], y_values = markets, type = 'unit_cost', max_output = 5)
        #self.unit_profit_mapping = MappingCard(name = 'Unit Profit', x_name = 'Unit Cost', y_name = 'Price', x_values = [1,2,3,4,5], y_values = prices, type = 'unit_profit', max_output = 5)
    
    def hire_employee(self, employee, sign_on_bonus = 0):
        self.capital -= sign_on_bonus
        self.employees.append(employee)

    def rent_building(self, building, deposit = 0):
        self.capital -= deposit
        self.buildings.append(building)

    def get_hand_dic(self, employee_cards = None, building_cards = None, price = None):
        emps = employee_cards if employee_cards != None else self.employees
        buds = building_cards if building_cards != None else self.buildings
        sel_prc = price if price != None else self.current_price

        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(emps)
        production, storage, desks, building_cost = self.get_building_attributes(buds)
        no_fac = int(production / self.game_settings.factory_to_prod)
        no_off = int(desks / self.game_settings.office_to_desk)
        return {'ops':operations, 'fin':finance, 'eng':engineering, 'mkt':marketing, 'dsk':desks, 'prd':production, 'prc':sel_prc}
    
    def analyse_game_state(self, hand_key, market_strength, total_desirability = -1, debug = 0):
        ops_emp, fin_emp, eng_emp, mkt_emp, no_off, no_fac, sel_prc = hand_key
        base_emp_val = self.game_settings.base_emp_value
        ops_emp = int(ops_emp / base_emp_val)
        fin_emp = int(fin_emp / base_emp_val)
        eng_emp = int(eng_emp / base_emp_val)
        mkt_emp = int(mkt_emp / base_emp_val)
        emps_cards, buds_cards = [], []
        
        base_emp_cost = self.game_settings.base_emp_cost
        for i in range(ops_emp):
            emps_cards.append(EmployeeCard(base_emp_val, 0, 0, 0, base_emp_cost))
        for i in range(fin_emp):
            emps_cards.append(EmployeeCard(0, base_emp_val, 0, 0, base_emp_cost))
        for i in range(eng_emp):
            emps_cards.append(EmployeeCard(0, 0, base_emp_val, 0, base_emp_cost))
        for i in range(mkt_emp):
            emps_cards.append(EmployeeCard(0, 0, 0, base_emp_val, base_emp_cost))
        for i in range(no_fac):
            val = self.game_settings.factory_to_prod
            cost = self.game_settings.factory_cost
            buds_cards.append(BuildingCard(val, 0, 0, cost))
        for i in range(no_off):
            val = self.game_settings.office_to_desk
            cost = self.game_settings.office_cost
            buds_cards.append(BuildingCard(0, 0, val, cost))
        net = self.calculate_net(emps_cards, buds_cards, sel_prc, market_strength, total_desirability, debug)
        return net

    def get_employee_attributes(self, employees):
        operations, engineering, finance, marketing, cost = 0, 0, 0, 0, 0
        for employee in employees:
            operations += employee.operations
            engineering += employee.engineering
            finance += employee.finance
            marketing += employee.marketing
            cost += employee.cost
        return operations, engineering, finance, marketing, cost
    
    def get_building_attributes(self, buildings):
        production, storage, desks, cost = 0, 0, 0, 0
        for building in buildings:
            production += building.production
            storage += building.storage
            desks += building.desks
            cost += building.cost
        return production, storage, desks, cost
    
    def calculate_desirability(self, employees, price, debug = 0):
        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(employees)
        brand = 0
        if marketing in self.game_settings.marketing_to_brand:
            brand = self.game_settings.marketing_to_brand[marketing]
        else:
            brand = max(self.game_settings.marketing_to_brand.values())
        if price in self.game_settings.price_to_price_des:
            price_desirability = self.game_settings.price_to_price_des[price]
        else:
            if debug:
                print('invalid company: price is not allowed')
            return False, 0

        price_des_plus_brand = brand + price_desirability
        if price_des_plus_brand in self.game_settings.price_des_plus_brand_to_desirability:
            desirability = self.game_settings.price_des_plus_brand_to_desirability[price_des_plus_brand]
        else:
            if debug:
                print('invalid company: price desirabilty or brand is invalid')
            return False, 0
        
        return True, desirability

    def calculate_desirability_new(self, employees, price = None, market_strength = None, debug = 0):
        if price == None:
            price = self.current_price
        if market_strength == None:
            market_strength = self.market
        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(employees)
        product_strength = self.product_mapping.get_value(marketing, price)
        desirability = self.demand_mapping.get_value(product_strength, market_strength)
        return True, desirability

    def calculate_net(self, employees, buildings, price, market_strength, total_desirability, debug = 0):
        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(employees)
        production, storage, desks, building_cost = self.get_building_attributes(buildings)
        total_cost = employee_cost + building_cost

        # mapping
        unit_cost, brand, max_gross, max_buildings = 0, 0, 0, 0
        if operations in self.game_settings.operations_to_max_buildings:
            max_buildings = self.game_settings.operations_to_max_buildings[operations]
        else:
            max_buildings = max(self.game_settings.operations_to_max_buildings.values())
            
        if marketing in self.game_settings.marketing_to_brand:
            brand = self.game_settings.marketing_to_brand[marketing]
        else:
            brand = max(self.game_settings.marketing_to_brand.values())
            
        if finance in self.game_settings.finance_to_max_gross:
            max_gross = self.game_settings.finance_to_max_gross[finance]
        else:
            max_gross = max(self.game_settings.finance_to_max_gross.values())
            
        if engineering in self.game_settings.engineering_to_unit_cost:
            unit_cost = self.game_settings.engineering_to_unit_cost[engineering]
        else:
            unit_cost = max(self.game_settings.engineering_to_unit_cost.values())
        
        # check these are valid combinations
        if len(buildings) > max_buildings:
            if debug:
                print('invalid company: too many buildings: ' + str(len(buildings)) + ', max buildings: ' + str(max_buildings))
            return False, 0
        
        if price in self.game_settings.price_to_price_des:
            price_desirability = self.game_settings.price_to_price_des[price]
        else:
            if debug:
                print('invalid company: price is not allowed')
            return False, 0
        
        if len(employees) > desks:
            if debug:
                print('invalid company: too many employees: ' + str(len(employees)) + ', desks: ' + str(desks))
            return False, 0
        
        # product desirability (brand + price desirability -> desirability)
        price_des_plus_brand = price_desirability + brand  # 2,3,4,5,6,7,8,9,10
        if price_des_plus_brand in self.game_settings.price_des_plus_brand_to_desirability:
            desirability = self.game_settings.price_des_plus_brand_to_desirability[price_des_plus_brand]
        else:
            if debug:
                print('invalid company: price desirabilty or brand is invalid')
            return False, 0
        
        # calculate demand (desirability -> demand)
        if total_desirability == -1:
            total_desirability = desirability # this is the test case or a single player game
        
        demand = self.market.get_player_demand(market_strength, total_desirability, desirability, False)
        units_sold = min([production, demand])
        unit_profit = price - unit_cost
        potential_gross = units_sold * unit_profit
        actual_gross = min([potential_gross, max_gross])
        net = actual_gross - total_cost
        if debug:
            print(' ---- A. max buildings: ' + str(max_buildings) + ', max employees: ' + str(desks) + ', max gross: ' + str(max_gross))
            print(' ---- B. (price desirability: ' + str(price_desirability) + ' + brand desirability: ' + str(brand) + ') -> desirability: ' + str(desirability))
            print(' ---- C. market strength: ' + str(market_strength) + ' -> total desirability: ' + str(total_desirability) + ' -> desirability: ' + str(desirability) + ' -> player demand: ' + str(demand) + '/' + str(production))
            print(' ---- D. (price: ' + str(price) + ' - unit cost: ' + str(unit_cost) + ') = unit profit: ' + str(unit_profit) + ' x units sold: ' + str(units_sold) + ' = potential gross: ' + str(potential_gross) + '/' + str(max_gross))
            print(' ---- E. (actual gross: ' + str(actual_gross) + ' - total cost: ' + str(total_cost) +  ') = net income: ' + str(net))
            
        return True, int(net)

    def calculate_net_new(self, employees, buildings, price = None, market_strength = None, total_demand = None, debug = 0):
        if price == None:
            price = self.current_price
        if market_strength == None:
            market_strength = self.market

        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(employees)
        production, storage, desks, building_cost = self.get_building_attributes(buildings)
        total_cost = employee_cost + building_cost

        # company properties
        product_strength = self.product_mapping.get_value(marketing, price)
        demand = self.demand_mapping.get_value(product_strength, market_strength)
        unit_cost = self.unit_cost_mapping.get_value(engineering, market_strength)
        unit_profit = self.unit_profit_mapping.get_value(unit_cost, price)

        # maxes
        unit_cost, max_gross, max_buildings = 0, 0, 0
        if operations in self.game_settings.operations_to_max_buildings:
            max_buildings = self.game_settings.operations_to_max_buildings[operations]
        else:
            max_buildings = max(self.game_settings.operations_to_max_buildings.values())
            
        if len(buildings) > max_buildings:
            if debug:
                print('invalid company: too many buildings: ' + str(len(buildings)) + ', max buildings: ' + str(max_buildings))
            return False, 0
        if len(employees) > desks:
            if debug:
                print('invalid company: too many employees: ' + str(len(employees)) + ', desks: ' + str(desks))
            return False, 0

        if finance in self.game_settings.finance_to_max_gross:
            max_gross = self.game_settings.finance_to_max_gross[finance]
        else:
            max_gross = max(self.game_settings.finance_to_max_gross.values())
        
        if total_demand == -1:
            total_demand = demand # this is the test case or a single player game
        
        # this needs to change to use the new demand -> units sold mapping cards
        units_sold = self.market.get_player_demand(market_strength, total_demand, demand, False)


        potential_gross = demand * unit_profit
        actual_gross = min([potential_gross, max_gross])
        net = actual_gross - total_cost
        if debug:
            print(' ---- A. max buildings: ' + str(max_buildings) + ', max employees: ' + str(desks) + ', max gross: ' + str(max_gross))
            print(' ---- B. (marketing: ' + str(marketing) + ' -> price: ' + str(price) + ' -> product strength: ' + str(product_strength))
            print(' ---- C. product strength: ' + str(product_strength) + ' -> market strength: ' + str(market_strength) + ' -> demand: ' + str(demand) + ' -> total demand: ' + str(total_demand) + ' -> unit sold: ' + str(units_sold))
            print(' ---- D. (price: ' + str(price) + ' - unit cost: ' + str(unit_cost) + ') = unit profit: ' + str(unit_profit) + ' x units sold: ' + str(units_sold) + ' = potential gross: ' + str(potential_gross) + '/' + str(max_gross))
            print(' ---- E. (actual gross: ' + str(actual_gross) + ' - total cost: ' + str(total_cost) +  ') = net income: ' + str(net))
            
        return True, int(net)
    
    def render(self):
        fig, axs = plt.subplots(2, 2)
        fig.set_figwidth(6)
        fig.set_figheight(6)
        fig.suptitle('Player Company') # or plt.suptitle('Main title')
        self.product_mapping.render(ax = axs[0][0])
        self.demand_mapping.render(ax = axs[1][0])
        self.unit_profit_mapping.render(ax = axs[0][1])
        self.unit_cost_mapping.render(ax = axs[1][1])

class Settings:
    def __init__(self, 
                 base_emp_value = 1,
                 emp_cost = 1,
                 bud_cost = 1,
                 no_players_to_board_size = {1:16, 2:20, 3:24, 4:28},
                 no_players_to_no_sell_cards = {1:4, 2:4, 3:6, 4:8},
                 no_players_to_no_commerce_cards = {1:4, 2:5, 3:6, 4:7},
                 no_players_to_no_industry_cards = {1:4, 2:5, 3:6, 4:7},
                 no_players_to_no_farm_cards = {1:4, 2:5, 3:6, 4:7},
                 no_players_to_no_residential_cards = {1:4, 2:5, 3:6, 4:7},
                 hq_allowed_on = ['commerce','industry'],
                 weak_buy_market_allowed_on = ['commerce','farm'],
                 strong_buy_market_allowed_on = ['farm'],
                 weak_sell_market_allowed_on = ['commerce','residential'],
                 strong_sell_market_allowed_on = ['residential'],
                 process_allowed_on = ['industry'],

                 no_players_to_no_buy_cards = {1:4, 2:4, 3:6, 4:8},
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
        self.no_players_to_no_sell_cards = no_players_to_no_sell_cards
        self.no_players_to_no_buy_cards = no_players_to_no_buy_cards

        self.no_players_to_no_commerce_cards = no_players_to_no_commerce_cards
        self.no_players_to_no_industry_cards = no_players_to_no_industry_cards
        self.no_players_to_no_farm_cards = no_players_to_no_farm_cards
        self.no_players_to_no_residential_cards = no_players_to_no_residential_cards

        self.hq_allowed_on = hq_allowed_on
        self.weak_buy_market_allowed_on = weak_buy_market_allowed_on
        self.strong_buy_market_allowed_on = strong_buy_market_allowed_on
        self.weak_sell_market_allowed_on = weak_sell_market_allowed_on
        self.strong_sell_market_allowed_on = strong_sell_market_allowed_on
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
    def __init__(self, game_settings, company):
        self.game_settings = game_settings

        self.company = company
        self.no_emp_cards_in_pool = game_settings.no_emp_cards_in_pool
        self.no_bud_cards_in_pool = game_settings.no_bud_cards_in_pool

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

class Market:
    def __init__(self, game_settings):
        self.game_settings = game_settings

        self.min_market_strength = 1
        self.current_strength = game_settings.starting_market_strength
        self.max_market_strength = 4

    def apply_market_move(self, market_move):
        self.current_strength = max([self.min_market_strength, min([self.max_market_strength, self.current_strength + market_move])])

class Board:
    def __init__(self, game_settings, no_players, cards, style = 'rectangle'):
        self.game_settings = game_settings
        self.no_players = no_players
        self.size = game_settings.no_players_to_board_size[no_players]
        if self.size != len(cards):
            raise Exception('Board Error: board size does not match number of cards')
        self.style = style
        self.cards = cards
        self.array = self.gen_board(self.size, style)
        self.location_to_card_index, self.card_index_to_location = self.gen_board_indices(self.array)
        
    def __str__(self):
        s = ''
        for r in range(len(self.array)):
            s2 = ''
            for c in range(len(self.array[0])):
                card_str = '| '
                if self.array[r][c] == 1:
                    card_index = self.location_to_card_index[(r,c)]
                    card_str += str(self.cards[card_index])
                else:
                    card_str += '  '
                card_str += ' |'
                s2 += card_str
            
            s += s2 + '\n'
            s = s.replace('||', '|').replace('  |  ', '     ')
        return s

    def gen_board(self, size, style):
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
     
    def render(self):
        fig, axs = plt.subplots(self.board_size, self.board_size)
        fig.set_figwidth(3.5 * self.board_size)
        fig.set_figheight(3.5 * self.board_size)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].render(ax = axs[i][j])

class Game:
    def __init__(self, game_settings, no_players, board_style = 'rectangle',theme = 'theme_0', shuffle = True, debug = 0):
        self.asset_path = join('assets', theme)
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings
        self.turn_number = 0

        # building cards - this is a deck that will be taken from arbitrarily
        self.weak_buy_market_cards = self.gen_building_cards(100, game_settings.buy_card_name, 'weak_buy_market', game_settings.weak_buy_market_allowed_on, 'Total Spend', 'Player Spend', [2,3,4,5,6,7,8], [1,2,3,4], 2, 5)
        self.strong_buy_market_cards = self.gen_building_cards(100, game_settings.buy_card_name, 'strong_buy_market', game_settings.strong_buy_market_allowed_on, 'Total Spend', 'Player Spend', [2,3,4,5,6,7,8], [1,2,3,4], 2, 7)
        self.weak_sell_market_cards = self.gen_building_cards(100, game_settings.sell_card_name, 'weak_sell_market', game_settings.weak_sell_market_allowed_on, 'Total Price', 'Player Price', [4,5,6,7,8,9,10], [2,3,4,5,4], 2, 5)
        self.strong_sell_market_cards = self.gen_building_cards(100, game_settings.sell_card_name, 'strong_sell_market', game_settings.strong_sell_market_allowed_on, 'Total Price', 'Player Price', [4,5,6,7,8,9,10], [2,3,4,5,4], 2, 7)
        self.process_cards = self.gen_building_cards(100, game_settings.process_card_name, 'process', game_settings.process_allowed_on, 'Connected ' + game_settings.buy_card_name, 'Connected ' + game_settings.sell_card_name, [0,1,2], [0,1,2], 1, 10)
        self.hq_cards = self.gen_building_cards(100, 'HQ', 'hq', game_settings.hq_allowed_on, 'Max Buildings', 'Max Employees', [0,3,6,9], [0,3,6,9], 1, 5)
        
        # board cards
        no_farm_cards = game_settings.no_players_to_no_farm_cards[no_players]
        no_residential_cards = game_settings.no_players_to_no_residential_cards[no_players]
        no_commerce_cards = game_settings.no_players_to_no_commerce_cards[no_players]
        no_industry_cards = game_settings.no_players_to_no_industry_cards[no_players]
        farm_cards = self.gen_board_cards(no_farm_cards, 'Farm', 'farm', 4)
        residential_cards = self.gen_board_cards(no_residential_cards, 'Residential', 'residential', 4)
        commerce_cards = self.gen_board_cards(no_commerce_cards, 'Commerce', 'commerce', 4)
        industry_cards = self.gen_board_cards(no_industry_cards, 'Industry', 'industry', 4)
        board_cards = farm_cards + residential_cards + commerce_cards + industry_cards
        if shuffle:
            board_cards = Deck(board_cards).shuffle()
        
        # board
        self.board = Board(game_settings, no_players, board_cards, board_style)
        
        # set up game entities
        #self.market = Market(game_settings)
        #self.players = [Player(game_settings, self.companies[i]) for i in range(no_players)]

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
        
    def gen_board_cards(self, count, name, card_type, max_emps):
        cards = []
        for i in range(count):
            cards.append(BoardCard(name = name, card_type = card_type, max_emps = max_emps))
        return cards

    def gen_building_cards(self, count, name, card_type, allowed_on, x_name, y_name, x_values, y_values, max_players, max_output):
        cards = []
        for i in range(count):
            cards.append(BuildingCard(name = name, card_type = card_type, x_name = x_name, y_name = y_name, x_values = x_values, y_values = y_values, max_players = max_players, max_output = max_output))
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
