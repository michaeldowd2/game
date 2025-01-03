import random
import copy
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import  join

ART_PATH = 'images/game_art'

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
        traits = ['Diligent', 'Hard-Worker', 'Positive', 'Creative', 'Smart', 'Thoughtful']
        return random.sample(traits, 2)
    
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
        l4 = 'Traits: '
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
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.employees = []
        self.buildings = []
        self.allowed_prices = [i for i in game_settings.price_to_demand]
        self.current_price = 5
        self.capital = game_settings.player_starting_cap
        self.engineering_to_unit_cost = game_settings.engineering_to_unit_cost
        self.marketing_to_brand = game_settings.marketing_to_brand
        self.finance_to_max_gross = game_settings.finance_to_max_gross
        self.operations_to_max_buildings = game_settings.operations_to_max_buildings
        self.price_to_demand = game_settings.price_to_demand
                
    def hire_employee(self, employee, sign_on_bonus = 0):
        self.capital -= sign_on_bonus
        self.employees.append(employee)

    def rent_building(self, building, deposit = 0):
        self.capital -= deposit
        self.buildings.append(building)

    def analyse_game_state(self, game_state, debug = 0):
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
        net = self.calculate_net(emps_cards, buds_cards, sel_prc, None, debug)
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
    
    def calculate_net(self, employees, buildings, price, demand_str_dict, debug = 0):
        operations, engineering, finance, marketing, employee_cost = self.get_employee_attributes(employees)
        production, storage, desks, building_cost = self.get_building_attributes(buildings)
        
        total_cost = employee_cost + building_cost

        # mapping
        unit_cost, brand, max_gross, max_buildings = 0, 0, 0, 0
        if operations in self.operations_to_max_buildings:
            max_buildings = self.operations_to_max_buildings[operations]
        else:
            max_buildings = max(self.operations_to_max_buildings.values())
            
        if marketing in self.marketing_to_brand:
            brand = self.marketing_to_brand[marketing]
        else:
            brand = max(self.marketing_to_brand.values())
            
        if finance in self.finance_to_max_gross:
            max_gross = self.finance_to_max_gross[finance]
        else:
            max_gross = max(self.finance_to_max_gross.values())
            
        if engineering in self.engineering_to_unit_cost:
            unit_cost = self.engineering_to_unit_cost[engineering]
        else:
            unit_cost = max(self.engineering_to_unit_cost.values())
        
        # check these are valid combinations
        if len(buildings) > max_buildings:
            print('invalid company: too many buildings: ' + str(len(buildings)) + ', max buildings: ' + str(max_buildings))
            return False, 0
        
        if price in self.price_to_demand:
            price_demand = self.price_to_demand[price]
        else:
            print('invalid company: price is not allowed')
            return False, 0
        
        if len(employees) > desks:
            print('invalid company: too many employees: ' + str(len(employees)) + ', desks: ' + str(desks))
            return False, 0
        
        # calculate net
        demand_str = brand + price_demand # 2,3,4,5,6,7,8,9,10
        #if demand_str not in demand_str_dict:
        #    print('invalid company: demand is not allowed')
        #    return False, 0
        actual_demand = demand_str # demand_str_dict[demand_str]
        units_sold = min([production, actual_demand])
        unit_profit = price - unit_cost
        potential_gross = units_sold * unit_profit
        actual_gross = min([potential_gross, max_gross])
        net = actual_gross - total_cost
        if debug:
            print('A, employees: ' + str(len(employees)) + '/' + str(desks) + ', operations: ' + str(operations) + ', engineering: ' + str(engineering) + ', finance: ' + str(finance) + ', marketing: ' + str(marketing))
            print('B, buildings: ' + str(len(buildings)) + '/' + str(max_buildings) + ', production: ' + str(production) + ', desks: ' + str(desks))
            print('C, price: ' + str(price) + ', price demand: ' + str(price_demand) + ', brand demand: ' + str(brand) + ', demand strength: ' + str(demand_str) + ', actual demand: ' + str(actual_demand))
            print('D, unit cost: ' + str(unit_cost) + ', unit profit: ' + str(unit_profit) + ', units sold: ' + str(units_sold))
            print('E, gross income: ' + str(potential_gross) + '/' + str(max_gross) + ', actual gross: ' + str(actual_gross) + ', total cost: ' + str(total_cost) +  ', net: ' + str(net))
            
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
                 price_to_demand = {1:6,2:5,3:4,4:3,5:2},
                 no_emp_cards_in_pool = 8,
                 no_emp_cards_per_attr = 16, 
                 no_bud_cards_in_pool = 4,
                 no_bud_cards_per_attr = 8,
                 player_starting_cap = 10,
                 market_values = [1,2,3,4,5,6,7,8,9,10],
                 starting_market_value = 3,
                 market_up_one_cards = 16,
                 market_up_two_cards = 4,
                 market_down_one_cards = 8,
                 market_down_two_cards = 2
                 ):
        
        # card properties
        self.base_emp_value = base_emp_value
        self.base_emp_cost = base_emp_cost
        self.factory_to_prod = factory_to_prod
        self.factory_cost = factory_cost
        self.office_to_desk = office_to_desk
        self.office_cost = office_cost
        # mappings for income function
        self.engineering_to_unit_cost = engineering_to_unit_cost
        self.marketing_to_brand = marketing_to_brand
        self.finance_to_max_gross = finance_to_max_gross
        self.operations_to_max_buildings = operations_to_max_buildings
        self.price_to_demand = price_to_demand
        # deck properties
        self.no_emp_cards_in_pool = no_emp_cards_in_pool
        self.no_emp_cards_per_attr = no_emp_cards_per_attr
        self.no_bud_cards_in_pool = no_bud_cards_in_pool
        self.no_bud_cards_per_attr = no_bud_cards_per_attr
        # player properties
        self.player_starting_cap = player_starting_cap
        # global market properties
        self.market_values = market_values
        self.starting_market_value = starting_market_value
        self.market_up_one_cards = market_up_one_cards
        self.market_up_two_cards = market_up_two_cards
        self.market_down_one_cards = market_down_one_cards
        self.market_down_two_cards = market_down_two_cards

class Player:
    def __init__(self, game_settings):
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

    def find_move(self, company, available_employees, available_buildings, remaining_employee_cards, remaining_building_cards, debug = 0):
        best_net, best_combo, best_price = -10000, [], 5
        current_net = company.calculate_net(company.employees, company.buildings, company.current_price, debug)

        test_combos = self.generate_doubles(len(available_employees))
        for test_combo in test_combos:
            test_emps = copy.deepcopy(company.employees)
            for ind in test_combo:
                test_emps.append(available_employees[ind])
            
            for price in company.allowed_prices:
                test_net = company.calculate_net(test_emps, price, False)
                if debug > 1 and price == 5:
                    print('Testing price: ' + str(price) + ', combination: Current Deck + ' + str(test_combo) + ', deck size: ' + str(len(test_emps)) + ', net: ' + str(test_net) + ', test_net: ' + str(test_net))
                if test_net > best_net:
                    best_net = test_net
                    best_combo = test_combo
                    best_price = price
                    if debug > 1:
                        print('new best set, best possible net: ' + str(best_net) + ', best combo: ' + str(best_combo) + ', best price: ' + str(best_price))
        if debug:
            print('best net income achieved: ' + str(best_net) + ', by hiring employees at indices: ' + str(best_combo) + ' and setting price to: ' + str(best_price))
            for ind in best_combo:
                test_emps = copy.deepcopy(company.employees)
                test_emps.append(available_employees[ind])
            test_net = company.calculate_net(test_emps, best_price, True)
        return best_combo, best_price, best_net

    def generate_move_combinations(self, available_cards, max_combos = 2 ):
        res = []
        for i in range(available_cards):
            res.append([i])
            for j in range(i, available_cards):
                if i != j:
                    res.append([i,j])
        return res
    
    def generate_game_states(self, game_settings, company, iterations = 100, debug = 0):
        desks_per_office = game_settings.office_to_desk

        ops_emp_ls = list(game_settings.operations_to_max_buildings.keys())
        all_fin_emps = list(game_settings.finance_to_max_gross.keys())
        all_eng_emps = list(game_settings.engineering_to_unit_cost.keys())
        all_mkt_emps = list(game_settings.marketing_to_brand.keys())

        max_fin = max(list(game_settings.finance_to_max_gross.keys()))
        max_eng = max(list(game_settings.engineering_to_unit_cost.keys()))
        max_mkt = max(list(game_settings.marketing_to_brand.keys()))

        res, x, y = {}, 0, 0
        # set up lists for each attribute
        row_keys, ops_ls, fin_ls, eng_ls, mkt_ls, off_ls, fac_ls, prc_ls, cst_ls, net_ls = [], [], [], [], [], [], [], [], [], []
        while x < iterations and y < 50000:
            ops_emp, eng_emp, fin_emp, mkt_emp = 0, 0, 0, 0
            # choose random number of ops employees
            ops_emp = random.choice(ops_emp_ls)

            # get max buildings based on ops employees
            max_buildings = game_settings.operations_to_max_buildings[ops_emp]

            # get min required offices based on ops employees
            min_offices = math.ceil(ops_emp / desks_per_office)

            # pick random combinations of buildings that are allowed
            no_off = random.randint(min_offices, max_buildings)
            no_fac = random.randint(0, max_buildings - no_off)

            # pick random remaining employees
            max_remaining_emp = no_off * desks_per_office * game_settings.base_emp_value - ops_emp
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
            unit_cost = game_settings.engineering_to_unit_cost[eng_emp]
            pos_prc_ls = list(game_settings.price_to_demand.keys())
            pos_prc_ls = [x for x in pos_prc_ls if x > unit_cost]
            if pos_prc_ls == [] or pos_prc_ls == None:
                continue # if unit cost = price this isn't worth considering
            sel_prc = random.choice(pos_prc_ls)
            
            key = [ops_emp, fin_emp, eng_emp, mkt_emp, no_off, no_fac, sel_prc]
            key = tuple(key)
            # build player hand from random combinations
            if key not in res:
                row_keys.append(key)
                ops_ls.append(ops_emp)
                fin_ls.append(fin_emp)
                eng_ls.append(eng_emp)
                mkt_ls.append(mkt_emp)
                off_ls.append(no_off)
                fac_ls.append(no_fac)
                prc_ls.append(sel_prc)
                cst_ls.append(unit_cost)
                net = company.analyse_game_state(key, debug)
                net_ls.append(net[1])
                res[key] = net
                if debug > 1:
                    print('iteration: ' + str(x) + ', new net for key: ' + str(key) + ', net: ' + str(net))
                x += 1
            else:
                if debug > 1:
                    print('iteration: ' + str(x) + ', existing net for key: ' + str(key) + ', net: ' + str(net))
            y += 1
        
        # create pandas dataframe
        df = pd.DataFrame({'gamestate key':row_keys, 'operations': ops_ls, 'finance': fin_ls, 'engineering': eng_ls, 'marketing': mkt_ls, 'offices': off_ls, 'factories': fac_ls, 'unit cost': cst_ls, 'price': prc_ls, 'net income': net_ls})
        
        return df

class GlobalMarket:
    def __init__(self, game_settings, no_players = 1):
        self.game_settings = game_settings
        self.market_demand_mappings = self.generate_market_demand_mappings() # turn -> total_demand_str -> player_demand_str -> player demand
        self.max_demand_str_player = max(list(self.game_settings.price_to_demand.keys())) + max(list(self.game_settings.brand_to_demand.keys()))
        self.min_demand_str_player = min(list(self.game_settings.price_to_demand.keys())) + min(list(self.game_settings.brand_to_demand.keys()))
        self.max_demand_str_tot = self.max_demand_str_player * self.no_players
        self.min_demand_str_tot = self.min_demand_str_player * self.no_players

    def generate_market_demand_mappings(self):
        market_value_mappings = {}
        for market_value in self.market_values:
            tot_demand_str = {}
            for tot_demand_str in range(self.min_demand_str_tot, self.max_demand_str_tot + 1):
                player_demand_str = {}
                for player_demand_str in range(self.min_demand_str_player, self.max_demand_str_player + 1):
                    demand = math.ceil(player_demand_str / tot_demand_str)
                    player_demand_str[player_demand_str] = demand
                tot_demand_str[tot_demand_str] = player_demand_str
            market_value_mappings[market_value] = tot_demand_str   
        return market_value_mappings

    def get_market_demand(self, market_value, tot_demand_str, player_demand_str):
        return self.market_demand_mappings[market_value][tot_demand_str][player_demand_str]
    
    def render(self, save_path = ''):
        pass

class Game:
    def __init__(self, game_settings, no_players, debug = 0):
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings

        self.market_deck = self.build_market_deck()
        self.employee_deck = self.build_employee_deck()
        self.building_deck = self.build_building_deck()
        self.players = [Player(game_settings) for i in range(no_players)]
        self.companies = [Company(game_settings) for i in range(no_players)]

    def build_market_deck(self):
        markets = ['market_up','market_down','market_big_up','market_big_down']
        art_imgs, art_idxs, art_max_idxs = {}, {}, {}
        for market in markets:
            art_imgs[market] = listdir(join(ART_PATH, market))
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
                art_img = art_imgs[market][art_idxs[market]]
                if art_idxs[market] < art_max_idxs[market] - 1:
                    art_idxs[market] += 1
                else:
                    art_idxs[market] = 0
                cards.append(MarketCard(value, join(ART_PATH, market, art_img)))
        return Deck(cards)
    
    def build_employee_deck(self):
        # employee art images
        genders = ['male','female']
        art_imgs, art_idxs = {}, {}
        for gender in genders:
            art_imgs[gender] = listdir(join(ART_PATH, 'employees_' + gender))
            art_idxs[gender] = 0
        
        emps = []
        for i in range(self.game_settings.no_emp_cards_per_attr):
            for attribute in ['operations', 'engineering', 'finance', 'marketing']:
                att_dic = {'operations':0, 'engineering':0, 'finance':0, 'marketing':0}
                att_dic[attribute] = self.game_settings.base_emp_value
                cost = self.game_settings.base_emp_cost

                # get next art image
                gender = random.choice(genders)
                art_img = art_imgs[gender][art_idxs[gender]]
                if art_idxs[gender] < len(art_imgs[gender]) - 1:
                    art_idxs[gender] += 1
                else:
                    art_idxs[gender] = 0
                
                emps.append(EmployeeCard(att_dic['operations'], att_dic['engineering'], att_dic['finance'], att_dic['marketing'], cost = cost, gender = gender, image_path =  join(ART_PATH, 'employees_' + gender, art_img)))
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
