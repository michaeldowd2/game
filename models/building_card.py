"""Building card model for game structures."""
from typing import Dict, List, Tuple, Optional
from .card import Card

class BuildingCard(Card):
    """A card representing a building in the game."""
    
    def __init__(self, name: str = '', card_type: str = '', x_name: str = '', 
                 y_name: str = '', max_output: int = 5, max_min: int = 2, 
                 max_players: int = 1, allowed_board_cards: List[str] = None) -> None:
        """Initialize a building card.
        
        Args:
            name: Name of the building
            card_type: Type of building (buy_market, sell_market, process, hq)
            x_name: Label for x-axis values
            y_name: Label for y-axis values
            max_output: Maximum output value
            max_min: Maximum minimum value
            max_players: Maximum number of players allowed
            allowed_board_cards: List of board card types this building can be placed on
        """
        super().__init__(name, card_type)
        valid_building_card_types = ['none', 'buy_market', 'sell_market', 'process', 'hq']
        if self.card_type not in valid_building_card_types:
            raise ValueError(f'Invalid card type: {self.card_type}')

        self.x_name = x_name
        self.y_name = y_name
        self.allowed_board_cards = allowed_board_cards or []
        self.max_players = max_players
        self.max_output = max_output
        self.max_min = max_min
        self.values, self.x_values, self.y_values = self.generate_values()
        self.title = self.name

    def get_value(self, x: int, y: int) -> int:
        """Get the value at coordinates (x,y).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Value at the specified coordinates
        """
        if x in self.x_values and y in self.y_values:
            return self.values[x][y]
        
        if x not in self.x_values:
            x = min(self.x_values) if x < min(self.x_values) else max(self.x_values)
        if y not in self.y_values:
            y = min(self.y_values) if y < min(self.y_values) else max(self.y_values)
        return self.values[x][y]
    
    def generate_values(self) -> Tuple[Dict[int, Dict[int, int]], List[int], List[int]]:
        """Generate value matrix based on card type.
        
        Returns:
            Tuple containing:
            - Dictionary of x,y coordinates to values
            - List of valid x values
            - List of valid y values
        """
        if self.card_type == 'buy_market':
            return self.generate_buy_market_values()
        elif self.card_type == 'sell_market':
            return self.generate_sell_market_values()
        elif self.card_type == 'process':
            return self.generate_process_values()
        else:
            return {}, [], []

    def generate_process_values(self) -> Tuple[Dict[int, Dict[int, int]], List[int], List[int]]:
        """Generate values for process type buildings."""
        res = {
            0: {0:0, 1:2, 2:4},
            1: {0:2, 1:4, 2:6},
            2: {0:4, 1:6, 2:8}
        }
        return res, [0,1,2], [0,1,2]

    def generate_sell_market_values(self) -> Tuple[Dict[int, Dict[int, int]], List[int], List[int]]:
        """Generate values for sell market type buildings."""
        res = {
            2: {2:6, 4:4, 5:5, 6:6, 7:7},
            3: {3:4, 4:2, 5:3, 6:4, 7:5, 8:6},
            4: {4:2, 5:1, 6:2, 7:3, 8:4, 9:5},
            5: {7:1, 8:2, 9:3, 10:4}
        }
        return res, [2,3,4,5], [2,3,4,5,6,7,8,9,10]
    
    def generate_buy_market_values(self) -> Tuple[Dict[int, Dict[int, int]], List[int], List[int]]:
        """Generate values for buy market type buildings."""
        res = {
            1: {1:5, 2:4, 3:3, 4:2, 5:1},
            2: {2:6, 3:5, 4:4, 5:3, 6:2},
            3: {3:7, 4:6, 5:5, 6:4, 7:3},
            4: {4:8, 5:7, 6:6, 7:5, 8:4}
        }
        return res, [1,2,3,4], [1,2,3,4,5,6,7,8]

    def render(self, ax = None, save_path: str = '') -> None:
        """Render the building card.
        
        Args:
            ax: Matplotlib axis object
            save_path: Path to save the rendered image
        """
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

    def str_render(self) -> None:
        """Prints the building card to the console."""
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
        """String representation of the building card.
        
        Returns:
            Formatted string with card details
        """
        if self.card_type == 'buy_market':
            return 'B'
        elif  self.card_type == 'sell_market':
            return 'S'
        elif self.card_type == 'process':
            return 'P'
        elif self.card_type == 'hq':
            return 'H'
        elif self.card_type == 'none':
            return '-'
        return ''