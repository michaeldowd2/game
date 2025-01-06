import random
import copy
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import join
from matplotlib import patches

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def take_N(self, N, render = False):
        res = []
        for i in range(N):
            x = random.choice(self.cards)
            self.cards.remove(x)
            res.append(x)
        return res
    
    def render(self, cards):
        fig, axs = plt.subplots(1, len(cards))
        fig.set_figwidth(15)
        
        for i, card in enumerate(cards):
            card.render(ax = axs[i])

    def remove_X(self, Card):
        self.cards.remove(Card)

    def take_N_from_bottom(self, N):
        res = self.cards[0:N]
        self.employees = self.employees[N:]
        return res

    def add_N_to_bottom(self, cards):
        self.cards = cards + self.cards

    def take_N_from_top(self, N):
        res = self.cards[len(self.cards)-N:]
        self.cards = self.cards[0:len(self.cards)-N]
        return res
    
    def add_N_to_top(self, cards):
        self.cards = self.cards + cards       
    
    def shuffle(self):
        random.shuffle(self.employees)

class BuildingCard:       
    def __init__(self, production = 0, storage = 0, desks = 0, cost = 2):
        self.cost = cost
        self.production = production
        self.storage = storage
        self.desks = desks
        self.attributes = {'production': production, 'storage': storage, 'desks': desks}
        self.type = self.get_type()
    
    def get_type(self):
        max_val, max_attr = 0, ''
        for attribute in ['production', 'storage', 'desks']:
            if self.attributes[attribute] > max_val:
                max_val = self.attributes[attribute]
                max_attr = attribute
        if max_attr == 'production':
            return 'factory'
        elif max_attr == 'storage':
            return 'warehouse'
        elif max_attr == 'desks':
            return 'office'
        else:
            return ''

    def __str__(self):
        return 'building, type: ' + self.type + ', cost: ' + str(self.cost) + ', production: ' + str(self.production) + ', storage: ' + str(self.storage) + ', desks: ' + str(self.desks)

    def render(self):
        pass

class EmployeeCard:
    def __init__(self, operations = 0, finance = 0, engineering = 0, marketing = 0, cost = 1, gender = 'male', image_path = ''):
        self.cost = cost
        self.operations = operations
        self.finance = finance
        self.engineering = engineering
        self.marketing = marketing
        self.attributes = {'operations': operations, 'finance': finance, 'engineering': engineering, 'marketing': marketing}
        self.department = self.get_department()
        self.gender = gender
        self.name = self.random_name()
        self.traits = self.random_traits()
        self.image_path = image_path

    def get_department(self):
        max_val, max_attr = 0, ''
        for attribute in ['operations', 'finance', 'engineering', 'marketing']:
            if self.attributes[attribute] > max_val:
                max_val = self.attributes[attribute]
                max_attr = attribute
        if max_attr == 'operations':
            return 'operations'
        elif max_attr == 'finance':
            return 'finance'
        elif max_attr == 'engineering':
            return 'engineering'
        elif max_attr == 'marketing':
            return 'marketing'
        else:
            return ''
    
    def random_traits(self):
        skills = ['Creative', 'Smart', 'Communication']
        return random.sample(skills, 2)
    
    def random_name(self):
        first_names_male=('John','Andy','Joe','Tom','Michael','Tim','Bob','Frank','Sam','Jim','James','Lou','Conor','Jack','Mick','Ronald','Alphonse')
        first_names_female=('Sam','Lou','Jill','Serena','Jenny','Kate','Lily','Grace','Mary','Jane','Helen','Natalie','Nancy','Sally','Eve','Emily')
        last_names=('Johnson','Smith','Williams','McGrath','Dowd','Sinclair','Frank','Roberts','O Shea','Wallace','Jones','Stevens','Sinclair')
        if self.gender == 'male':
            return random.choice(first_names_male) + " " + random.choice(last_names)
        else:
            return random.choice(first_names_female) + " " + random.choice(last_names)
    
    def render(self, ax = None, save_path = ''):
        low_res_props = {'w':256, 'h':339, 'p':4, 'r':22, 'fs1': 9, 'fs2': 10, 'fs3': 8}
        high_res_props = {'w':1024, 'h':1365, 'p':12, 'r':94, 'fs1': 36, 'fs2': 40, 'fs3': 28}

        props = low_res_props
        if save_path != '' or ax == None: # create a full resolution axis
            props = high_res_props

        w, h, p, r = props['w'], props['h'], props['p'], props['r']
        csfont = {'fontname':'consolas'}

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

        # set string values
        l1 = 'O: ' + str(self.operations) + ', F: ' + str(self.finance) + ', E: ' + str(self.engineering) + ', M: ' + str(self.marketing) + ', $' + str(self.cost)
        l2 = 'Name: ' + self.name
        l3 = 'Department: ' + self.department.capitalize()
        l4 = 'Skills: '
        for trait in self.traits:
            l4 += trait + ', '
        l4 = l4[:-2]
        
        # add to plot
        ax.text(p, h-p, l1, fontsize=props['fs1'], ha='left', va='top',**csfont)
        ax.text(p, h-r, l2, fontsize=props['fs2'], ha='left', va='top',**csfont)
        ax.text(p, h-2*r, l3, fontsize=props['fs2'], ha='left', va='top',**csfont)
        ax.text(p, w+p, l4, fontsize=props['fs3'], ha='left', va='bottom',**csfont)
        
        if save_path != '':
            plt.savefig(save_path, dpi=100, bbox_inches='tight') 

        # return current figure
        return plt 
        
    def __str__(self):
        return 'employee, name: ' + self.name + ', department: ' + self.department + ', cost: ' + str(self.cost) + ', operations: ' + str(self.operations) + ', finance: ' + str(self.finance) + ', engineering: ' + str(self.engineering) + ', marketing: ' + str(self.marketing)

class MarketCard:
    def __init__(self, value, image_path = ''):
        self.value = value
        self.image_path = image_path

        self.name = self.get_random_event()
        self.description =      'Upwards shift in global demand'
        if value == 2:
            self.description =  'Big Up move in global demand'
        elif value == -1:
            self.description =  'Downwards shift in global demand'
        elif value == -2:
            self.description =  'Big Down move in global demand'

    def __str__(self):
        return 'Market Card: ' + str(self.name) + ', value: ' + str(self.value)
    
    def render(self, ax = None, save_path = ''):
        low_res_props = {'w':256, 'h':339, 'p':6, 'r':24, 'fs1': 9, 'fs2': 10, 'fs3': 8}
        high_res_props = {'w':1024, 'h':1365, 'p':12, 'r':94, 'fs1': 36, 'fs2': 40, 'fs3': 28}

        props = low_res_props
        if save_path != '' or ax == None: # create a full resolution axis
            props = high_res_props

        w, h, p, r = props['w'], props['h'], props['p'], props['r']
        csfont = {'fontname':'consolas'}

        if ax == None:
            plt.figure(figsize=(w/100, h/100), dpi=100)
            ax = plt.gca()
        
        ax.set_xlim(0, w)
        ax.get_xaxis().set_ticks([])
        ax.set_ylim(0, h)
        ax.get_yaxis().set_ticks([])
        
        if self.image_path != '':
            print('img path: ' + self.image_path)
            img = plt.imread(self.image_path)
            imgplot = ax.imshow(img, extent=(0, w, 0, w))
        else:
            imgplot = ax.imshow(np.zeros((w, w)), extent=(0, w, 0, w))

        # set string values
        plus = ''
        if self.value > 0:
            plus = '+ '
        l1 = 'Market Move: ' + plus + str(self.value)
        l2 = self.name
        l3 = self.description
        
        # add to plot
        ax.text(p, h - p, l1, fontsize=props['fs1'], ha='left', va='top',**csfont)
        ax.text(p, h - p - r, l2, fontsize=props['fs2'], ha='left', va='top',**csfont)
        ax.text(p, h - p - 2 * r, l3, fontsize=props['fs3'], ha='left', va='top',**csfont)
        
        if save_path != '':
            plt.savefig(save_path, dpi=100, bbox_inches='tight') 

        # return current figure
        return plt 
    
    def get_random_event(self):
        if self.value == 1:
            return random.choice(['Economic Growth','Technological Advancements','Low Interest Rates','Quantitative Easing','Tax Cuts','Population Growth', 'Energy Price Decreases','Monetary Policy Loosening'])
        elif self.value == -1:
            return random.choice(['Recession','Automation and Job Losses','Energy Price Increases','Monetary Policy Tightening','Austerity Measures'])
        elif self.value == -2:
            return random.choice(['Financial Crisis', 'Supply Chain Disruptions', 'War Breaks Out', 'Trade Tarrifs', 'Pandemic'])
        elif self.value == 2:
            return random.choice(['Economic Boom', 'Stock Market Boom','New Tech Discovery','New Resources Discovered'])
        return ''

class Company:
    def __init__(self, game_settings, market):
        self.game_settings = game_settings
        self.market = market
        self.employees = []
        self.buildings = []
        self.current_price = 5
        self.capital = game_settings.player_starting_cap
                
    def hire_employee(self, employee, sign_on_bonus = 0):
        self.capital -= sign_on_bonus
        self.employees.append(employee)

    def rent_building(self, building, deposit = 0):
        self.capital -= deposit
        self.buildings.append(building)

    def analyse_game_state(self, game_state, market_strength, total_desirability = -1, debug = 0):
        ops_emp, fin_emp, eng_emp, mkt_emp, no_off, no_fac, sel_prc = game_state
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
            print('invalid company: price is not allowed')
            return False, 0

        price_des_plus_brand = brand + price_desirability
        if price_des_plus_brand in self.game_settings.price_des_plus_brand_to_desirability:
            desirability = self.game_settings.price_des_plus_brand_to_desirability[price_des_plus_brand]
        else:
            print('invalid company: price desirabilty or brand is invalid')
            return False, 0
        
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
            print('invalid company: too many buildings: ' + str(len(buildings)) + ', max buildings: ' + str(max_buildings))
            return False, 0
        
        if price in self.game_settings.price_to_price_des:
            price_desirability = self.game_settings.price_to_price_des[price]
        else:
            print('invalid company: price is not allowed')
            return False, 0
        
        if len(employees) > desks:
            print('invalid company: too many employees: ' + str(len(employees)) + ', desks: ' + str(desks))
            return False, 0
        
        # product desirability (brand + price desirability -> desirability)
        price_des_plus_brand = brand + price_desirability # 2,3,4,5,6,7,8,9,10
        if price_des_plus_brand in self.game_settings.price_des_plus_brand_to_desirability:
            desirability = self.game_settings.price_des_plus_brand_to_desirability[price_des_plus_brand]
        else:
            print('invalid company: price desirabilty or brand is invalid')
            return False, 0
        
        # calculate demand (desirability -> demand)
        if total_desirability == -1:
            total_desirability = desirability # this is the test case or a single player game
        
        demand = self.market.get_player_demand(market_strength, total_desirability, desirability)
        units_sold = min([production, demand])
        unit_profit = price - unit_cost
        potential_gross = units_sold * unit_profit
        actual_gross = min([potential_gross, max_gross])
        net = actual_gross - total_cost
        if debug:
            print('A. employees: ' + str(len(employees)) + '/' + str(desks) + ', operations: ' + str(operations) + ', engineering: ' + str(engineering) + ', finance: ' + str(finance) + ', marketing: ' + str(marketing))
            print('B. buildings: ' + str(len(buildings)) + '/' + str(max_buildings) + ', production: ' + str(production) + ', desks: ' + str(desks))
            print('C. (price desirability: ' + str(price) + ' + brand desirability: ' + str(brand) + ') -> desirability: ' + str(desirability))
            print('D. market strength: ' + str(market_strength) + ' -> total desirability: ' + str(total_desirability) + ' -> desirability: ' + str(desirability) + ' -> demand: ' + str(demand) + '/' + str(production))
            print('E. (price: ' + str(price) + ' - unit cost: ' + str(unit_cost) + ') = unit profit: ' + str(unit_profit) + ' x units sold: ' + str(units_sold) + ' = potential gross: ' + str(potential_gross) + '/' + str(max_gross))
            print('F. (actual gross: ' + str(actual_gross) + ' - total cost: ' + str(total_cost) +  ') = net income: ' + str(net))
            
        return True, net

class GameSettings:
    def __init__(self, 
                 base_emp_value = 1,
                 base_emp_cost = 0.5,
                 factory_to_prod = 4,
                 factory_cost = 1,
                 office_to_desk = 4,
                 office_cost = 1,
                 engineering_to_unit_cost = {0:5,1:4,2:3,3:2,4:1},
                 marketing_to_brand = {0:2,1:3,2:4,3:5,4:6},
                 finance_to_max_gross = {0:4,1:8,2:16,3:24,4:32},
                 operations_to_max_buildings = {0:2,1:3,2:4,3:5,4:6},
                 price_to_price_des =  {1:8,2:7,3:6,4:5,5:4},
                 price_des_plus_brand_to_desirability = {2:1,3:1,4:2,5:2,6:3,7:3,8:4,9:4,10:5},
                 no_emp_cards_in_pool = 8,
                 no_emp_cards_per_attr = 16, 
                 no_bud_cards_in_pool = 4,
                 no_bud_cards_per_attr = 8,
                 market_strength_to_demand = {1:4,2:8,3:12,4:16,5:20,6:24},
                 starting_market_strength = 3,
                 market_up_one_cards = 16,
                 market_up_two_cards = 4,
                 market_down_one_cards = 8,
                 market_down_two_cards = 2,
                 player_starting_cap = 10,
                 no_of_turns_in_game = 12
                 ):
        
        # card properties
        self.base_emp_value = base_emp_value
        self.base_emp_cost = base_emp_cost
        self.factory_to_prod = factory_to_prod
        self.factory_cost = factory_cost
        self.office_to_desk = office_to_desk
        self.office_cost = office_cost

        # mappings for income function
        self.price_to_price_des = price_to_price_des
        self.engineering_to_unit_cost = engineering_to_unit_cost
        self.marketing_to_brand = marketing_to_brand
        self.finance_to_max_gross = finance_to_max_gross
        self.operations_to_max_buildings = operations_to_max_buildings
        self.price_des_plus_brand_to_desirability = price_des_plus_brand_to_desirability
        
        # deck properties
        self.no_emp_cards_in_pool = no_emp_cards_in_pool
        self.no_emp_cards_per_attr = no_emp_cards_per_attr
        self.no_bud_cards_in_pool = no_bud_cards_in_pool
        self.no_bud_cards_per_attr = no_bud_cards_per_attr

        # global market properties
        self.allowed_market_strength_values = [i for i in market_strength_to_demand] # set allowed prices from the mapping dict
        self.allowed_desirability_values = list(set([price_des_plus_brand_to_desirability[i] for i in price_des_plus_brand_to_desirability])) # list of product desirability values
        self.market_strength_to_demand = market_strength_to_demand
        self.starting_market_strength = starting_market_strength
        self.market_up_one_cards = market_up_one_cards
        self.market_up_two_cards = market_up_two_cards
        self.market_down_one_cards = market_down_one_cards
        self.market_down_two_cards = market_down_two_cards

        # player properties
        self.player_starting_cap = player_starting_cap
        self.no_of_turns_in_game = no_of_turns_in_game

class Player:
    def __init__(self, game_settings, company):
        self.game_settings = game_settings
        self.company = company
        self.no_emp_cards_in_pool = game_settings.no_emp_cards_in_pool
        self.no_bud_cards_in_pool = game_settings.no_bud_cards_in_pool

    def build_probable_pool(self, available_cards, no_emp_cards_in_pool = 8, no_bud_cards_in_pool = 6):
        card_class = available_cards[0].__class__.__name__
        pool_size = no_emp_cards_in_pool
        if card_class != 'EmployeeCard':
            pool_size = no_bud_cards_in_pool

        attributes = []
        for attribute in available_cards[0].attributes:
            attributes.append(attribute)
        
        card_attribute_count = {}
        for card in available_cards:
            key = []
            for attribute in attributes:
                key.append(card.attributes[attribute])
            key = tuple(key)
            if key not in card_attribute_count:
                card_attribute_count[key] = 1
            else:
                card_attribute_count[key] += 1
        
        sorted_counts = dict(sorted(card_attribute_count.items(), key=lambda item: item[1]))
        likely_pool, likelihood, count = [], [], 0
        for key in sorted_counts:
            if card_class == 'EmployeeCard':
                likely_pool.append(EmployeeCard(key[0], key[1], key[2], key[3]))
            else:
                likely_pool.append(BuildingCard(key[0], key[1], key[2]))
            likelihood.append(sorted_counts[key] / len(available_cards))
            count += 1
            if count > pool_size:
                break
        return likely_pool, likelihood

    def find_move(self, company, available_employees, available_buildings, market_strength, total_desirability = -1, debug = 0):
        test_emp_idx_combos = self.generate_doubles(len(available_employees)) # hire up to two employees per turn
        test_bud_idxs = range(len(available_buildings)) # pick up to one building per turn
        test_prices = list(self.game_settings.price_to_price_des.keys())
        
        best_net, best_emp_combo, best_bud_idx, best_price = -10000, [], 5
        for test_emp_idx_combo in test_emp_idx_combos:
            test_emps = copy.deepcopy(company.employees)
            for test_emp_idx in test_emp_idx_combo:
                test_emps.append(available_employees[test_emp_idx])

            for bud_idx in test_bud_idxs:
                test_buds = copy.deepcopy(company.buildings)
                test_buds.append(available_buildings[bud_idx])
            
                for test_price in test_prices:
                    test_net = company.calculate_net(test_emps, test_buds, test_price, market_strength, total_desirability, False)
                    if debug > 1:
                        print('Testing price: ' + str(test_price) + ', test emp idxs + ' + str(test_emp_idx_combo) + ', test bud idx: ' + str(bud_idx) + ', net: ' + str(test_net))
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
    def __init__(self, game_settings, no_players = 1, image_path = ''):
        self.game_settings = game_settings
        self.no_players = no_players
        self.current_strength = game_settings.starting_market_strength
        self.market_strength_mappings = self.generate_market_strength_mappings() # turn -> total_demand_str -> player_demand_str -> player demand
        self.image_path = image_path

    def generate_market_strength_mappings(self):
        min_player_product_desirability = min(self.game_settings.allowed_desirability_values)
        max_Player_product_desirability = max(self.game_settings.allowed_desirability_values)
        min_total_product_desirability = min_player_product_desirability # fill in dictionary to support a minimum of one player
        max_total_product_desirability = max_Player_product_desirability * 4 # fill in dictionary to support a maximum of four players

        market_strength_mappings = {}
        for market_strength in self.game_settings.market_strength_to_demand:
            market_demand = self.game_settings.market_strength_to_demand[market_strength] # total market demand at this level
            total_desirability_to_demand = {}
            for total_desirability in range(min_total_product_desirability, max_total_product_desirability + 1):
                player_desirability_to_demand = {}
                for player_desirability in range(min_player_product_desirability, max_Player_product_desirability + 1):
                    player_desirability_to_demand[player_desirability] = math.ceil(market_demand * player_desirability / total_desirability)
                total_desirability_to_demand[total_desirability] = player_desirability_to_demand
            market_strength_mappings[market_strength] = total_desirability_to_demand   
        return market_strength_mappings

    def get_player_demand(self, market_strength, total_desirability, player_desirability, debug = 0):
        if debug:
            print('market stength: ' + str(market_strength) + ', total desirability: ' + str(total_desirability) + ', player desirability: ' + str(player_desirability))
        return self.market_strength_mappings[market_strength][total_desirability][player_desirability]
    
    def render(self, ax = None, save_path = ''):
        if self.image_path != '':
            print('here')
            imgs = listdir(join(self.image_path, 'board'))
            no_imgs = len(imgs)
            if no_imgs > 0:
                f1s = 20
                f2s = 32
                p = 128
                no_market_strengths = 4 # len(self.game_settings.market_strength_to_demand)
                max_players =  4
                w, h = 760 * no_market_strengths + 2 * p, 760 * max_players + 2 * p

                csfont = {'fontname':'consolas'}

                if ax == None:
                    plt.figure(figsize=(w/100, h/100), dpi=100)
                    ax = plt.gca()
            
                ax.set_xlim(0, w)
                ax.get_xaxis().set_ticks([])
                ax.set_ylim(0, h)
                ax.get_yaxis().set_ticks([])
            
                count = 0

                for i in range(no_market_strengths):
                    #market strength ruler
                    rect = patches.Rectangle((p+i*760, h - p), 760, p, linewidth=1, edgecolor='black', facecolor='none')
                    ax.add_patch(rect)
                    ax.text(p+i*760+380, h-12, 'Market Strength: ' + str(i+1), fontsize=f1s, ha='center', va='top',**csfont)


                    for j in range(max_players):
                        x0, y0, x1, y1 = p+i*760, p+j*760, p+i*760 + 760, p+j*760+760
                        img_idx = count % no_imgs
                        img = plt.imread(join(self.image_path, 'board', imgs[img_idx]))
                        imgplot = ax.imshow(img, extent=(x0,x1,y0,y1))
                        count += 1
                max_desirability = max(self.game_settings.allowed_desirability_values)
                #draw rectangle
                for i in range(no_market_strengths):
                    for j in range(max_players):
                        w, h = 113, 113        
                        x0, y0 = p + i * 760, p + j * 760 + 195
                        
                        for x in range(len(self.game_settings.allowed_desirability_values)):
                            x_mods = {0:0,1:0,2:-6,3:-10,4:0} # modify start points of rectangles
                            w_mods = {0:0,1:-6,2:-4,3:10,4:0} # modify widths of rectangles
                            x_mod, w_mod = 0, 0
                            if x in x_mods:
                                x_mod = x_mods[x]
                            if x in w_mods:
                                w_mod = w_mods[x]
                            start_x = x0 + 113 * x + x_mod
                            width = 113 + w_mod
                            for y in range(len(self.game_settings.allowed_desirability_values)):
                                y_mods = {0:0,1:2,2:8,3:4,4:2} # modify start points of rectangles
                                h_mods = {0:2,1:6,2:-4,3:-2,4:-2} # modify heights of rectangles
                                y_mod, h_mod = 0, 0
                                if y in y_mods:
                                    y_mod = y_mods[y]
                                if y in h_mods:
                                    h_mod = h_mods[y]
                                start_y = y0 + 113 * y + y_mod
                                height = 113 + h_mod

                                rect = patches.Rectangle((start_x, start_y), width, height, linewidth=1, edgecolor='black', facecolor='white', alpha = 0.2)
                                ax.add_patch(rect)
                                text = str(self.market_strength_mappings[i+1][j*max_desirability+y+1][x+1]) # str(i+1) + ', ' + str(j*max_desirability+y+1) + ', ' + str(x+1) + ', ' + str(self.market_strength_mappings[i+1][j*max_desirability+y+1][x+1])
                                ax.text(start_x + width/2, start_y+height/2, text, fontsize=f2s, ha='center', va='center',**csfont, color = 'black')
                if save_path != '':
                    plt.savefig(save_path, dpi=100, bbox_inches='tight') 


class Game:
    def __init__(self, game_settings, no_players, theme = 'theme_0', debug = 0):
        self.asset_path = join('assets', theme)
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings

        self.market_deck = self.build_market_deck()
        self.employee_deck = self.build_employee_deck()
        self.building_deck = self.build_building_deck()

        self.market = Market(game_settings, image_path = self.asset_path)
        self.companies = [Company(game_settings, self.market) for i in range(no_players)]
        self.players = [Player(game_settings, self.companies[i]) for i in range(no_players)]

    def start(self):
        for turn in range(len(self.game_settings.no_of_turns_in_game)):
            self.run_turn()

    def run_turn(self):
        pass

    def build_market_deck(self):
        markets = ['market_up','market_down','market_big_up','market_big_down']
        art_imgs, art_idxs, art_max_idxs = {}, {}, {}
        for market in markets:
            art_imgs[market] = listdir(join(self.asset_path, market))
            art_idxs[market] = 0
            art_max_idxs[market] = len(art_imgs[market])
        
        cards = []
        for market in markets:
            no_cards = self.game_settings.market_up_one_cards
            value = 1
            if market == 'market_big_up':
                no_cards = self.game_settings.market_up_two_cards
                value = 2
            elif market == 'market_down':
                no_cards = self.game_settings.market_down_one_cards
                value = -1
            elif market == 'market_big_down':
                no_cards = self.game_settings.market_down_two_cards
                value = -2
            for i in range(no_cards):
                art_img = ''
                if len(art_imgs[market]) > 0:
                    idx = art_idxs[market] % len(art_imgs[market])
                    art_img = join(self.asset_path, market, art_imgs[market][idx]) 
                    art_idxs[market] += 1
                cards.append(MarketCard(value, art_img))
        return Deck(cards)
    
    def build_employee_deck(self):
        # employee art images
        genders = ['male','female']
        art_imgs, art_idxs = {}, {}
        for gender in genders:
            art_imgs[gender] = listdir(join(self.asset_path, 'employees_' + gender))
            art_idxs[gender] = 0
        
        emps, count = [], 0
        for i in range(self.game_settings.no_emp_cards_per_attr):
            for attribute in ['operations', 'engineering', 'finance', 'marketing']:
                att_dic = {'operations':0, 'engineering':0, 'finance':0, 'marketing':0}
                att_dic[attribute] = self.game_settings.base_emp_value
                cost = self.game_settings.base_emp_cost

                gender_ind, art_img = count % 2, ''
                gender = genders[gender_ind]
                if len(art_imgs[gender]) > 0:
                    idx = art_idxs[gender] % len(art_imgs[gender])
                    art_img = join(self.asset_path, 'employees_' + gender, art_imgs[gender][idx]) 
                    art_idxs[gender] += 1
                emps.append(EmployeeCard(att_dic['operations'], att_dic['engineering'], att_dic['finance'], att_dic['marketing'], cost = cost, gender = gender, image_path = art_img))
                count += 1
        return Deck(emps)

    def build_building_deck(self):
        buds = []
        for i in range(self.game_settings.no_bud_cards_per_attr):
            for attribute in ['production', 'storage', 'desks']:
                att_dic = {'production':0, 'storage':0, 'desks':0}
                cost = 1
                if attribute == 'desks':
                    att_dic['desks'] = self.game_settings.office_to_desk
                    cost = self.game_settings.office_cost
                elif attribute == 'production':
                    att_dic['production'] = self.game_settings.factory_to_prod
                    cost = self.game_settings.factory_cost
                buds.append(BuildingCard(att_dic['production'], att_dic['storage'], att_dic['desks'], cost=cost))
        return Deck(buds)
