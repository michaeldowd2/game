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

class MappingCard:
    def __init__(self, name = '', x_name = '', y_name = '', x_values = [], y_values = [], type = 'demand', max_output = 5, max_min = 2):
        self.name = name
        self.x_name = x_name
        self.y_name = y_name
        self.x_values = x_values
        self.y_values = y_values
        self.type = type
        self.max_output = max_output
        self.max_min = max_min
        self.values = self.generate_values()
        self.title = self.generate_title()
        self.subtitle = self.generate_subtitle()

        self.image_path = ''
        if os.path.exists(join(ASSET_PATH, self.type)):
            imgs = listdir(join(ASSET_PATH, self.type))
            img_idx = IMG_IDX[type]
            IMG_IDX[type] += 1
            self.image_path = join(ASSET_PATH, self.type, imgs[img_idx % len(imgs)])

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
    
    def generate_subtitle(self):
        return 'Cost: $2'
    
    def get_start_x_and_width(self, index):
        x_mod, w_mod, x_mods, w_mods = 0, 0, {0:0,1:0,2:-6,3:-10,4:0}, {0:0,1:-6,2:-4,3:10,4:0} # modify start points and widthsof rectangles
        if index in x_mods:
            x_mod = x_mods[index]
        if index in w_mods:
            w_mod = w_mods[index]
        return 113 * index + x_mod, 113 + w_mod
    
    def get_start_y_and_height(self, index):
        y_mod, h_mod, y_mods, h_mods = 0, 0, {0:0,1:2,2:8,3:4,4:2}, {0:2,1:6,2:-4,3:-2,4:-2} # modify start points and heights of rectangles
        if index in y_mods:
            y_mod = y_mods[index]
        if index in h_mods:
            h_mod = h_mods[index]
        return 113 * index + y_mod, 113 + h_mod

    def render(self, ax = None, save_path = ''):
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
            start_x, width = self.get_start_x_and_width(i)
            for j, y in enumerate(self.y_values):
                start_y, height = self.get_start_y_and_height(j)
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
        fig.set_figwidth(12)
        fig.set_figheight(3)
        
        for i, card in enumerate(cards):
            if card is not None:
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
        random.shuffle(self.cards)

class BuildingCard:       
    def __init__(self, production = 0, storage = 0, desks = 0, cost = 2, building_type = '', image_path = ''):
        self.cost = cost
        self.production = production
        self.storage = storage
        self.desks = desks
        self.attributes = {'production': production, 'storage': storage, 'desks': desks}

        self.type = building_type
        if building_type == '':
            self.type = self.get_type()
        self.image_path = image_path
    
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
        return 'p' + str(self.production) + ' d' + str(self.desks) + ' $' + str(self.cost)

    def render(self, ax = None, save_path = ''):
        low_res_props = {'w':256, 'h':339, 'p':4, 'r':22, 'fs1': 8, 'fs2': 10, 'fs3': 8}
        high_res_props = {'w':1024, 'h':1365, 'p':12, 'r':94, 'fs1': 34, 'fs2': 40, 'fs3': 28}

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
        l1 = 'Production: ' + str(self.production) + ', Desks: ' + str(self.desks) + ', $' + str(self.cost)
        l2 = 'Type: ' + self.type.capitalize()
        # add to plot
        ax.text(p, h-p, l1, fontsize=props['fs1'], ha='left', va='top',**csfont)
        ax.text(p, h-r, l2, fontsize=props['fs2'], ha='left', va='top',**csfont)
        
        if save_path != '':
            plt.savefig(save_path, dpi=100, bbox_inches='tight') 

        # return current figure
        return plt 

class EmployeeCard:
    def __init__(self, operations = 0, finance = 0, engineering = 0, marketing = 0, cost = 1, gender = 'male'):
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

        category = 'employees_' + self.gender
        imgs = listdir(join(ASSET_PATH, category))
        img_idx = IMG_IDX[category]
        IMG_IDX[category] += 1
        self.image_path = join(ASSET_PATH, category, imgs[img_idx % len(imgs)])

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
        low_res_props = {'w':256, 'h':339, 'p':4, 'r':26, 'fs1': 8, 'fs2': 9, 'fs3': 7}
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
        l2 = self.name
        l3 = self.department.capitalize()
        l4 = ''
        for trait in self.traits:
            l4 += trait + ', '
        l4 = l4[:-2]
        
        # add to plot
        ax.text(p, h-p, l1, fontsize=props['fs1'], ha='left', va='top',**csfont)
        ax.text(w/2, h-r, l2, fontsize=props['fs2'], ha='center', va='top',**csfont)
        ax.text(w/2, w+p+14, l3, fontsize=props['fs3'], ha='center', va='bottom',**csfont)
        ax.text(w/2, w+p, l4, fontsize=props['fs3'], ha='center', va='bottom',**csfont)
        
        if save_path != '':
            plt.savefig(save_path, dpi=100, bbox_inches='tight') 

        # return current figure
        return plt 
        
    def __str__(self):
        return 'o' + str(self.operations) + ' f' + str(self.finance) + ' e' + str(self.engineering) + ' m' + str(self.marketing) + ' $' + str(self.cost)

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
        return 'M: value: ' + str(self.value)
    
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
    def __init__(self, game_settings, market):
        self.game_settings = game_settings
        self.market = market
        self.employees = []
        self.buildings = []
        self.current_price = 5
        self.capital = game_settings.player_starting_cap
        
        # mapping cards
        prices, markets = [4,5,6,7,8], [1,2,3,4,5]
        self.product_mapping = MappingCard(name = 'Product', x_name = 'Brand', y_name = 'Price', x_values = [1,2,3,4,5], y_values = prices, type = 'product', max_output = 5)
        self.demand_mapping = MappingCard(name = 'Demand: P', x_name = 'Product', y_name = 'Market', x_values = [1,2,3,4,5], y_values = markets, type = 'demand', max_output = 5)
        self.unit_cost_mapping = MappingCard(name = 'Unit Cost', x_name = 'Ops', y_name = 'Market', x_values = [1,2,3,4,5], y_values = markets, type = 'unit_cost', max_output = 5)
        self.unit_profit_mapping = MappingCard(name = 'Unit Profit', x_name = 'Unit Cost', y_name = 'Price', x_values = [1,2,3,4,5], y_values = prices, type = 'unit_profit', max_output = 5)
    
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

class GameSettings:
    def __init__(self, 
                 base_emp_value = 1,
                 base_emp_cost = 1,
                 factory_to_prod = 3,
                 factory_cost = 2,
                 office_to_desk = 4,
                 office_cost = 1,
                 engineering_to_unit_cost = {0:5,1:4,2:3,3:2,4:1},
                 marketing_to_brand = {0:1,1:2,2:3,3:4,4:5},
                 finance_to_max_gross = {0:4,1:12,2:24,3:36,4:48},
                 operations_to_max_buildings = {0:2,1:4,2:6,3:7,4:8},
                 price_to_price_des =  {1:5,2:4,3:3,4:2,5:1},
                 price_des_plus_brand_to_desirability = {2:1,3:1,4:2,5:2,6:3,7:3,8:4,9:4,10:5},
                 no_emp_cards_in_pool = 8,
                 no_emp_cards_per_attr = 16, 
                 no_bud_cards_in_pool = 4,
                 no_bud_cards_per_attr = 8,
                 market_strength_to_demand = {1:5,2:6,3:9,4:12,5:15,6:18,7:21,8:24},
                 player_no_to_market_strength_range = {1:(1,2,3), 2:(1,2,4), 3:(2,3,6), 4:(3,4,8)},
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
        self.player_no_to_market_strength_range = player_no_to_market_strength_range
        self.allowed_desirability_values = list(set([price_des_plus_brand_to_desirability[i] for i in price_des_plus_brand_to_desirability])) # list of product desirability values
        self.market_strength_to_demand = market_strength_to_demand
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
    def __init__(self, game_settings, no_players = 1, image_path = ''):
        self.game_settings = game_settings
        self.no_players = no_players
        self.market_strength_mappings = self.generate_market_strength_mappings() # turn -> total_demand_str -> player_demand_str -> player demand
        self.image_path = image_path

        self.min_market_strength = game_settings.player_no_to_market_strength_range[no_players][0]
        self.current_strength = game_settings.player_no_to_market_strength_range[no_players][1]
        self.max_market_strength = game_settings.player_no_to_market_strength_range[no_players][2]

    def apply_market_move(self, market_move):
        self.current_strength = max([self.min_market_strength, min([self.max_market_strength, self.current_strength + market_move])])

    def generate_market_strength_mappings(self):
        min_player_product_desirability = min(self.game_settings.allowed_desirability_values)
        max_Player_product_desirability = max(self.game_settings.allowed_desirability_values)
        min_total_product_desirability = min_player_product_desirability # fill in dictionary to support a minimum of one player
        max_total_product_desirability = max_Player_product_desirability * 4 # fill in dictionary to support a maximum of four players

        market_strength_mappings = {}
        for market_strength in self.game_settings.market_strength_to_demand:
            
            total_desirability_to_demand = {}
            for total_desirability in range(min_total_product_desirability, max_total_product_desirability + 1):
                player_desirability_to_demand = {}
                for player_desirability in range(min_player_product_desirability, max_Player_product_desirability + 1):
                    if player_desirability <= total_desirability and player_desirability + max_Player_product_desirability * (self.no_players - 1) >= total_desirability:
                        market_demand = self.game_settings.market_strength_to_demand[market_strength] # total market demand at this level
                        demand = int(market_demand * player_desirability / total_desirability)
                        #demand = max([1, demand])
                        #demand = min([demand, player_desirability])
                        player_desirability_to_demand[player_desirability] = demand
                total_desirability_to_demand[total_desirability] = player_desirability_to_demand
            market_strength_mappings[market_strength] = total_desirability_to_demand   
        return market_strength_mappings

    def get_player_demand(self, market_strength, total_desirability, player_desirability, debug = 0):
        if debug:
            print('market stength: ' + str(market_strength) + ', total desirability: ' + str(total_desirability) + ', player desirability: ' + str(player_desirability))
        return self.market_strength_mappings[market_strength][total_desirability][player_desirability]
    
    def render(self, ax = None, save_path = '', player_desirabilities = []):
        tot_player_desirability = sum(player_desirabilities)
        render_players = len(player_desirabilities) > 0
        player_cols = {0:'purple',1:'green',2:'blue',3:'red',4:'yellow',5:'orange'}

        if self.image_path != '':
            imgs = listdir(join(self.image_path, 'board'))
            no_imgs = len(imgs)
            fontsize1, fontsize2, padding, fontsize3 = 20, 28, 128, 24
            no_market_strengths = len(self.game_settings.market_strength_to_demand)
            max_players =  self.no_players
            max_player_des = max(self.game_settings.allowed_desirability_values)
            max_total_des = max_players * max(self.game_settings.allowed_desirability_values)
            w, h = 760 * no_market_strengths + 2 * padding, 760 * max_players + 2 * padding

            font = load_font(
                font_url="https://github.com/google/fonts/blob/main/apache/specialelite/SpecialElite-Regular.ttf?raw=true"
            )
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
                rect = patches.Rectangle((padding + i * 760, h - padding), 760, padding, linewidth = 1, edgecolor = 'black', facecolor = 'none')
                ax.add_patch(rect)
                ax.text(padding + i * 760 + 380, h - 12, 'Market Strength: ' + str(i+1), fontsize = fontsize1, ha = 'center', va = 'top', font = font) #**csfont)

                # draw images
                if no_imgs > 0:
                    for j in range(max_players):
                        x0, y0, x1, y1 = padding + i * 760, padding + j * 760, padding + i * 760 + 760, padding + j * 760 + 760
                        img_idx = count % no_imgs
                        img = plt.imread(join(self.image_path, 'board', imgs[img_idx]))
                        imgplot = ax.imshow(img, extent=(x0, x1, y0, y1))
                        count += 1
                
            for i in range(no_market_strengths):
                for j in range(max_players):
                    w, h = 113, 113        
                    x0, y0 = padding + i * 760, padding + j * 760 + 195
                    
                    for x in range(len(self.game_settings.allowed_desirability_values)):
                        desirability = x + 1

                        x_mod, w_mod, x_mods, w_mods = 0, 0, {0:0,1:0,2:-6,3:-10,4:0}, {0:0,1:-6,2:-4,3:10,4:0} # modify start points and widthsof rectangles
                        if x in x_mods:
                            x_mod = x_mods[x]
                        if x in w_mods:
                            w_mod = w_mods[x]
                        start_x = x0 + 113 * x + x_mod
                        width = 113 + w_mod

                        for y in range(len(self.game_settings.allowed_desirability_values)):
                            tot_desirability = j * max_player_des + y + 1

                            y_mod, h_mod, y_mods, h_mods = 0, 0, {0:0,1:2,2:8,3:4,4:2}, {0:2,1:6,2:-4,3:-2,4:-2} # modify start points and heights of rectangles
                            if y in y_mods:
                                y_mod = y_mods[y]
                            if y in h_mods:
                                h_mod = h_mods[y]
                            start_y = y0 + 113 * y + y_mod
                            height = 113 + h_mod

                            # y axis labels
                            if i == 0 and x == 0:
                                ax.text(start_x - 16, start_y + height / 2, str(tot_desirability), fontsize = fontsize3, ha = 'right', va = 'center', font = font)

                            # x axis labels
                            if tot_desirability == max_total_des:
                                ax.text(start_x + width / 2, start_y + height + 6, str(desirability), fontsize = fontsize3, ha = 'center', va = 'bottom', font = font)

                            # values
                            if desirability in self.market_strength_mappings[i + 1][tot_desirability] and self.market_strength_mappings[i + 1][tot_desirability][desirability] > 0:
                                rect = patches.Rectangle((start_x, start_y), width, height, linewidth=1, edgecolor='black', facecolor='white', alpha = 0.3)
                                ax.add_patch(rect)
                                text = str(self.market_strength_mappings[i + 1][tot_desirability][desirability])
                                ax.text(start_x + width / 2, start_y + height / 2, text, fontsize = fontsize2, ha = 'center', va = 'center', color = 'black', font = font)
                            
                            # draw player demands
                            offsets = [(-16, -16), (16, 16), (16, -16), (-16, 16), (-6,-6), (6,6)]
                            if render_players and self.current_strength == i+1 and tot_player_desirability == tot_desirability:
                                for p_ind in range(len(player_desirabilities)):
                                    player_desirability = player_desirabilities[p_ind]
                                    if player_desirability == desirability:
                                        off = offsets[p_ind]
                                        count = len([x for x in player_desirabilities if x == player_desirability])
                                        if count == 1:
                                            off = (0,0)
                                        col = player_cols[p_ind]
                                        circle = patches.Circle((start_x + off[0] + width / 2, start_y + off[1] + height / 2), radius = 36, linewidth = 2, edgecolor = 'black', facecolor = col, alpha=0.4)
                                        ax.add_patch(circle)
            
            if save_path != '':
                plt.savefig(save_path, dpi=100, bbox_inches='tight') 

class Board:
    def __init__(self, game_settings, no_players, image_path = ''):
        self.game_settings = game_settings
        self.no_players = no_players
        self.image_path = image_path
        self.board_size = 3
        self.no_cards = int(self.board_size * self.board_size)
        self.cards = self.generate_board_cards()
        self.board = self.generate_board(self.cards)

    def generate_board_cards(self):
        cards = []
        for i in range(self.board_size):
            cards.append(MappingCard(name = 'Materials District', x_name = 'Logistics', y_name = 'Supply', x_values = [1,2,3,4,5], y_values = [1,2,3,4,5], type = 'material_district', max_output = 5))
        for i in range(self.board_size):
            cards.append(MappingCard(name = 'Production District', x_name = 'Engineering', y_name = 'Factories', x_values = [1,2,3,4,5], y_values = [1,2,3,4,5], type = 'production_district', max_output = 5))
        for i in range(self.board_size):
            cards.append(MappingCard(name = 'Sales District', x_name = 'Product', y_name = 'Demand', x_values = [1,2,3,4,5], y_values = [1,2,3,4,5], type = 'sales_district', max_output = 5))
        random.shuffle(cards)
        return cards
    
    def generate_board(self, cards):
        rows, index = [], 0
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                row.append(cards[index])
                index += 1
            rows.append(row)
        return rows
    
    def render(self):
        fig, axs = plt.subplots(self.board_size, self.board_size)
        fig.set_figwidth(3.5 * self.board_size)
        fig.set_figheight(3.5 * self.board_size)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].render(ax = axs[i][j])

class Game:
    def __init__(self, game_settings, no_players, theme = 'theme_0', shuffle = True, apply_market_cards = True, debug = 0):
        self.asset_path = join('assets', theme)
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings
        self.turn_number = 0
        self.apply_market_cards = apply_market_cards

        # build decks
        self.market_deck = self.build_market_deck()
        #self.building_deck = self.build_building_deck()
        self.employee_deck = self.build_employee_deck()

        self.board = Board(game_settings, no_players, image_path = self.asset_path)
        
        # demand mapping deck
        #self.units_sold_mapping_deck = self.build_units_sold_mapping_deck()

        # shuffle decks
        if shuffle:
            self.market_deck.shuffle()
            #self.building_deck.shuffle()
            self.employee_deck.shuffle()

        # set up game entities
        self.market = Market(game_settings, no_players = no_players, image_path = self.asset_path)
        self.companies = [Company(game_settings, self.market) for i in range(no_players)]
        self.players = [Player(game_settings, self.companies[i]) for i in range(no_players)]

        # add starting cards
        for company in self.companies:
            company.rent_building(BuildingCard(game_settings.factory_to_prod, 0, 0, game_settings.factory_cost)) # add factory
            company.rent_building(BuildingCard(0, 0, game_settings.office_to_desk, game_settings.office_cost)) # add office

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
        market_card = self.market_deck.take_N_from_top(1)[0]
        building_pool = self.building_deck.take_N_from_top(self.game_settings.no_bud_cards_in_pool)
        employee_pool = self.employee_deck.take_N_from_top(self.game_settings.no_emp_cards_in_pool)

        # apply market move card
        if self.apply_market_cards:
            self.market.apply_market_move(market_card.value)
            new_market_val = self.market.current_strength

        if debug:
            building_pool_str, employee_pool_str = '-- BUD Pool | ', '-- EMP Pool | '
            i = 0
            for b in building_pool:
                building_pool_str += 'B' + str(i) + ' ' +str(b) + ' | '
                i += 1
            i = 0
            for e in employee_pool:
                employee_pool_str += 'E' + str(i) + ' ' + str(e) + ' | '
                i+=1
            print('-- MKT Card | ' + str(market_card) + ' | : Market Strength: ' + str(prev_market_val) + ' -> ' + str(new_market_val))
            print(building_pool_str + '\n' + employee_pool_str)

        if render:
            self.render_current_turn_cards(market_card, building_pool, employee_pool)

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
        
    def build_units_sold_mapping_deck(self):
        
        cards = []
        x_values = [1,2,3,4,5]
        y_combos = [[2,3,4,5,6], [2,3,4,5,6], [4,5,6,7,8], [4,5,6,7,8], [6,7,8,9,10], [6,7,8,9,10]]
        v_combos = [4, 6, 4, 6, 6, 8]
        for i in range(len(y_combos)):
            y_values, v = y_combos[i], v_combos[i]
            cards.append(MappingCard(name = 'Units Sold', x_name = 'Demand: P', y_name = 'Demand: T', x_values = x_values, y_values = y_values, type = 'shop', max_output = v))
        return Deck(cards)

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
        
        emps, count = [], 0
        for i in range(self.game_settings.no_emp_cards_per_attr):
            for attribute in ['operations', 'engineering', 'finance', 'marketing']:
                att_dic = {'operations':0, 'engineering':0, 'finance':0, 'marketing':0}
                att_dic[attribute] = self.game_settings.base_emp_value
                cost = self.game_settings.base_emp_cost

                gender = genders[count % 2]
                emps.append(EmployeeCard(att_dic['operations'], att_dic['engineering'], att_dic['finance'], att_dic['marketing'], cost = cost, gender = gender))
                count += 1
        return Deck(emps)

    def build_building_deck(self):
        buds, art_imgs, art_idxs  = [], {}, {}
        for bud_type in ['factory', 'office']:
            art_imgs[bud_type] = listdir(join(self.asset_path, 'buildings_' + bud_type))
            art_idxs[bud_type] = 0

        for i in range(self.game_settings.no_bud_cards_per_attr):
            for bud_type in ['factory', 'office']:
                att_dic, cost, art_img = {'production':0, 'storage':0, 'desks':0}, 1, ''
                if len(art_imgs[bud_type])>0:
                    idx = art_idxs[bud_type] % len(art_imgs[bud_type])
                    art_img = join(self.asset_path, 'buildings_' + bud_type, art_imgs[bud_type][idx]) 
                    art_idxs[bud_type] += 1

                if bud_type == 'office':
                    att_dic['desks'] = self.game_settings.office_to_desk
                    cost = self.game_settings.office_cost
                elif bud_type == 'factory':
                    att_dic['production'] = self.game_settings.factory_to_prod
                    cost = self.game_settings.factory_cost
                buds.append(BuildingCard(att_dic['production'], att_dic['storage'], att_dic['desks'], cost=cost, building_type = bud_type, image_path = art_img))
        return Deck(buds)

    def render_current_turn_cards(self, market_card, bud_cards, emp_cards):
        self.render_row_of_cards(['Market Card', 'Building Card Pool'],[market_card, None] + bud_cards)
        self.render_row_of_cards(['Employee Card Pool'], emp_cards)

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
