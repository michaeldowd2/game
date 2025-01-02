import random
import copy
import math
import pandas as pd
class Deck:
    def __init__(self, cards):
        self.cards = cards

    def take_N(self, N):
        res = []
        for i in range(N):
            x = random.choice(self.cards)
            self.cards.remove(x)
            res.append(x)
        return res

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
    def __init__(self, type):
        if type in ['factory','office','warehouse']:
            self.type = type
        self.cost = 2
        self.production = 0
        self.storage = 0
        self.desks = 0
        if type == 'factory':
            self.production = 3
        elif type == 'warehouse':
            self.storage = 4
        elif type == 'office':
            self.desks = 3
        self.attributes = {'production': self.production, 'storage': self.storage, 'desks': self.desks}
            
    def __init__(self, production = 0, storage = 0, desks = 0):
        self.cost = (production + storage + desks) * 2 / 3
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
    def __init__(self, department):
        self.name = self.random_name()
        if department in ['operations','finance','engineering','marketing']:
            self.department = department
        self.cost = 1
        self.operations = 0
        self.finance = 0
        self.engineering = 0
        self.marketing = 0
        if department == 'operations':
            self.operations = 1
        elif department == 'finance':
            self.finance = 1
        elif department == 'engineering':    
            self.engineering = 1
        elif department == 'marketing':
            self.marketing = 1
        self.attributes = {'operations': self.operations, 'finance': self.finance, 'engineering': self.engineering, 'marketing': self.marketing}

    def __init__(self, operations = 0, finance = 0, engineering = 0, marketing = 0):
        self.name = self.random_name()
        self.cost = operations + finance + engineering + marketing
        self.operations = operations
        self.finance = finance
        self.engineering = engineering
        self.marketing = marketing
        self.attributes = {'operations': operations, 'finance': finance, 'engineering': engineering, 'marketing': marketing}
        self.department = self.get_department()

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
    
    def random_name(self):
        first_names=('John','Andy','Joe','Tom','Michael','Tim','Bob','Frank','Sam','Jim','James','Lou','Conor','Jill','Jack','Serena','Mick','Ronald','Alphonse')
        last_names=('Johnson','Smith','Williams','McGrath','Dowd','Sinclair','Frank','Roberts','O Shea','Wallace','Jones','Stevens','Sinclair')
        name = random.choice(first_names) + " " + random.choice(last_names)
        return name
    
    def __str__(self):
        return 'employee, name: ' + self.name + ', department: ' + self.department + ', cost: ' + str(self.cost) + ', operations: ' + str(self.operations) + ', finance: ' + str(self.finance) + ', engineering: ' + str(self.engineering) + ', marketing: ' + str(self.marketing)
class Company:
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.employees = []
        self.buildings = []
        self.allowed_prices = [i for i in game_settings.price_to_demand]
        self.current_price = 5
        self.capital = game_settings.starting_capital
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
        emps_cards, buds_cards = [], []
        for i in range(ops_emp):
            emps_cards.append(EmployeeCard(1, 0, 0, 0))
        for i in range(fin_emp):
            emps_cards.append(EmployeeCard(0, 1, 0, 0))
        for i in range(eng_emp):
            emps_cards.append(EmployeeCard(0, 0, 1, 0))
        for i in range(mkt_emp):
            emps_cards.append(EmployeeCard(0, 0, 0, 1))
        for i in range(no_fac):
            production = self.game_settings.production_per_factory
            buds_cards.append(BuildingCard(production, 0, 0))
        for i in range(no_off):
            desks = self.game_settings.desks_per_office
            buds_cards.append(BuildingCard(0, 0, desks))
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
            print('A, employee attributes: operations: ' + str(operations) + ', engineering: ' + str(engineering) + ', finance: ' + str(finance) + ', marketing: ' + str(marketing))
            print('B, building attributes: production: ' + str(production) + ', storage: ' + str(storage) + ', desks: ' + str(desks) + ', max buildings: ' + str(max_buildings))
            print('C, unit cost: ' + str(unit_cost) + ', brand demand: ' + str(brand) + ', price demand: ' + str(price_demand) + ', demand strength: ' + str(demand_str) + ', actual demand: ' + str(actual_demand)) 
            print('D, potential gross: ' + str(potential_gross)  + ', max gross: ' + str(max_gross) + ', actual gross: ' + str(actual_gross) + ', total cost: ' + str(total_cost) +  ', net: ' + str(net))
            
        return True, net
class GameSettings:
    def __init__(self, 
                 no_emp_cards_in_pool,
                 no_emp_cards_per_attr, 
                 no_bud_cards_in_pool,
                 no_bud_cards_per_attr,
                 desks_per_office,
                 production_per_factory,
                 cost_per_office,
                 cost_per_factory,
                 starting_capital,
                 engineering_to_unit_cost,
                 marketing_to_brand,
                 finance_to_max_gross,
                 operations_to_max_buildings,
                 price_to_demand
                 ):
        self.no_emp_cards_in_pool = no_emp_cards_in_pool
        self.no_emp_cards_per_attr = no_emp_cards_per_attr
        self.no_bud_cards_in_pool = no_bud_cards_in_pool
        self.no_bud_cards_per_attr = no_bud_cards_per_attr
        self.desks_per_office = desks_per_office
        self.production_per_factory = production_per_factory
        self.cost_per_office = cost_per_office
        self.cost_per_factory = cost_per_factory
        self.starting_capital = starting_capital
        self.engineering_to_unit_cost = engineering_to_unit_cost
        self.marketing_to_brand = marketing_to_brand
        self.finance_to_max_gross = finance_to_max_gross
        self.operations_to_max_buildings = operations_to_max_buildings
        self.price_to_demand = price_to_demand
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
        cards = copy.deepcopy(available_cards)
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
        desks_per_office = game_settings.desks_per_office

        ops_emp_ls = list(game_settings.operations_to_max_buildings.keys())
        max_fin = max(list(game_settings.finance_to_max_gross.keys()))
        max_eng = max(list(game_settings.engineering_to_unit_cost.keys()))
        max_mkt = max(list(game_settings.marketing_to_brand.keys()))

        res, x, y = {}, 0, 0
        # set up lists for each attribute
        ops_ls, fin_ls, eng_ls, mkt_ls, off_ls, fac_ls, prc_ls, cst_ls, net_ls = [], [], [], [], [], [], [], [], []
        while x < iterations and y < 1000:

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
            max_remaining_emp = no_off * desks_per_office - ops_emp
            eng_emp = random.randint(0, min(max_eng, max_remaining_emp))
            fin_emp = random.randint(0, min(max_fin, max_remaining_emp - eng_emp))
            mkt_emp = random.randint(0, min(max_mkt, max_remaining_emp - eng_emp - fin_emp))

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
                ops_ls.append(ops_emp)
                fin_ls.append(fin_emp)
                eng_ls.append(eng_emp)
                mkt_ls.append(mkt_emp)
                off_ls.append(no_off)
                fac_ls.append(no_fac)
                prc_ls.append(sel_prc)
                cst_ls.append(unit_cost)

                emps_cards, buds_cards = [], []
                for i in range(ops_emp):
                    emps_cards.append(EmployeeCard(1, 0, 0, 0))
                for i in range(fin_emp):
                    emps_cards.append(EmployeeCard(0, 1, 0, 0))
                for i in range(eng_emp):
                    emps_cards.append(EmployeeCard(0, 0, 1, 0))
                for i in range(mkt_emp):
                    emps_cards.append(EmployeeCard(0, 0, 0, 1))
                for i in range(no_fac):
                    production = game_settings.production_per_factory
                    buds_cards.append(BuildingCard(production, 0, 0))
                for i in range(no_off):
                    desks = game_settings.desks_per_office
                    buds_cards.append(BuildingCard(0, 0, desks))

                net = company.calculate_net(emps_cards, buds_cards, sel_prc, debug)
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
        df = pd.DataFrame({'operations': ops_ls, 'finance': fin_ls, 'engineering': eng_ls, 'marketing': mkt_ls, 'offices': off_ls, 'factories': fac_ls, 'unit cost': cst_ls, 'price': prc_ls, 'net': net_ls})
        df = df.sort_values(by = 'net', ascending = False)
        return df
class Game:
    def __init__(self, game_settings, no_players, debug = 0):
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings

        self.employee_deck = self.build_employee_deck()
        self.building_deck = self.build_building_deck()
        self.players = [Player(game_settings) for i in range(no_players)]
        self.companies = [Company(game_settings) for i in range(no_players)]

    def build_employee_deck(self):
        emps = []
        for i in range(self.game_settings.no_emp_cards_per_attr):
            for attribute in ['operations', 'engineering', 'finance', 'marketing']:
                att_dic = {'operations':0, 'engineering':0, 'finance':0, 'marketing':0}
                att_dic[attribute] = 1
                emps.append(EmployeeCard(att_dic['operations'], att_dic['engineering'], att_dic['finance'], att_dic['marketing']))
        return Deck(emps)

    def build_building_deck(self):
        buds = []
        for i in range(self.game_settings.no_bud_cards_per_attr):
            for attribute in ['production', 'storage', 'desks']:
                att_dic = {'production':0, 'storage':0, 'desks':0}
                if attribute == 'production':
                    att_dic['production'] = self.game_settings.production_per_factory
                elif attribute == 'desks':
                    att_dic['desks'] = self.game_settings.desks_per_office
                else:
                    att_dic[attribute] = 3
                buds.append(BuildingCard(att_dic['production'], att_dic['storage'], att_dic['desks']))
        return Deck(buds)
