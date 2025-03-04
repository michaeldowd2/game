"""Game module containing the main Game class for managing game state and flow."""

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

from models.card import Card
from models.deck import Deck
from models.building_card import BuildingCard
from models.board_card import BoardCard
from models.settings import Settings
from models.board import Board
from models.player import Player

class Game:
    """Main game class that manages the game state and flow."""
    
    def __init__(self, game_settings: Settings, no_players: int, board_style: str = 'rectangle',
                 theme: str = 'theme_0', shuffle: bool = True, debug: int = 0):
        """Initialize the game.
        
        Args:
            game_settings: Game settings configuration
            no_players: Number of players
            board_style: Style of board layout
            theme: Visual theme to use
            shuffle: Whether to shuffle cards
            debug: Debug level
        """
        self.asset_path = join('assets', theme)
        self.debug = debug
        self.no_players = no_players
        self.game_settings = game_settings
        self.turn_number = 0
        
        # Initialize players
        self.players = [Player(i, game_settings) for i in range(no_players)]

        # Initialize building cards
        self.building_cards = self._init_building_cards()
        
        # Initialize board
        self.board = Board(game_settings, no_players, shuffle, board_style)

    def _init_building_cards(self) -> dict:
        """Initialize all building card decks.
        
        Returns:
            Dictionary containing different types of building cards
        """
        buy_market_cards = self.gen_building_cards(
            100, 
            self.game_settings.buy_card_name, 
            'buy_market',
            self.game_settings.buy_market_allowed_on,
            'Total Spend',
            'Player Spend',
            2, 5
        )
        
        sell_market_cards = self.gen_building_cards(
            100,
            self.game_settings.sell_card_name,
            'sell_market',
            self.game_settings.sell_market_allowed_on,
            'Total Price',
            'Player Price',
            2, 5
        )
        
        process_cards = self.gen_building_cards(
            100,
            self.game_settings.process_card_name,
            'process',
            self.game_settings.process_allowed_on,
            f'Connected {self.game_settings.buy_card_name}',
            f'Connected {self.game_settings.sell_card_name}',
            1, 10
        )
        
        hq_cards = self.gen_building_cards(
            100,
            'HQ',
            'hq',
            self.game_settings.hq_allowed_on,
            'Max Buildings',
            'Max Employees',
            1, 5
        )
        
        return {
            'buy_market': buy_market_cards,
            'sell_market': sell_market_cards,
            'process': process_cards,
            'hq': hq_cards
        }

    def gen_building_cards(self, count: int, name: str, card_type: str, 
                         allowed_on: list, x_name: str, y_name: str,
                         max_players: int, max_output: int) -> list:
        """Generate a list of building cards with specified parameters.
        
        Args:
            count: Number of cards to generate
            name: Name of the card
            card_type: Type of building card
            allowed_on: List of allowed board positions
            x_name: X-axis label name
            y_name: Y-axis label name
            max_players: Maximum number of players allowed
            max_output: Maximum output value
            
        Returns:
            List of generated BuildingCard objects
        """
        return [
            BuildingCard(
                name=name,
                card_type=card_type,
                x_name=x_name,
                y_name=y_name,
                max_players=max_players,
                max_output=max_output,
                allowed_board_cards=allowed_on
            )
            for _ in range(count)
        ]

    def render_row_of_cards(self, titles: list, cards: list) -> None:
        """Render a row of cards with titles.
        
        Args:
            titles: List of titles for the row
            cards: List of cards to render
        """
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
                card.render(ax=axs[i])
    
    def render_none(self, ax=None) -> None:
        """Render an empty card space.
        
        Args:
            ax: Matplotlib axis to render on
        """
        props = {'w': 256, 'h': 339, 'p': 6, 'r': 24, 'fs1': 9, 'fs2': 10, 'fs3': 8}
        w, h = props['w'], props['h']
        
        if ax is None:
            plt.figure(figsize=(w/100, h/100), dpi=100)
            ax = plt.gca()
        
        ax.set_xlim(0, w)
        ax.set_ylim(0, h)
        
        # Disable axis outlines and ticks
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
