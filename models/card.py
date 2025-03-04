"""Core card models for the game."""
from dataclasses import dataclass
from typing import List, Dict, Optional
import os
from os.path import join
from matplotlib import axes

@dataclass
class CardConfig:
    """Configuration for card properties."""
    asset_path: str = join('assets', 'theme_1')
    valid_card_types: List[str] = ('farm', 'residential', 'industry', 'unit_cost','sell_market', 'buy_market', 'process', 'hq')

class Card:
    """Base class for all game cards."""
    
    def __init__(self, name: str, card_type: str = '') -> None:
        """Initialize a card.
        
        Args:
            name: The name of the card
            card_type: The type of card, defaults to lowercase of name if not provided
        """
        self.name = name
        self.card_type = card_type.lower() if card_type else name.lower()
        self.image_path = self._set_image_path()
        
    def _set_image_path(self) -> str:
        """Set the image path for the card based on its type.
        
        Returns:
            str: Path to the card's image file
        """
        if not self.card_type or self.card_type not in CardConfig.valid_card_types:
            return ''
            
        path = join(CardConfig.asset_path, self.card_type)
        if not os.path.exists(path):
            return ''
            
        imgs = os.listdir(path)
        if not imgs:
            return ''
            
        # Get next image index for this card type
        from ..utils.image_manager import get_next_image_index
        img_idx = get_next_image_index(self.card_type)
        return join(CardConfig.asset_path, self.card_type, imgs[img_idx % len(imgs)])
        
    def render(self, ax: Optional[axes.Axes] = None) -> None:
        """Render the card.
        
        Args:
            ax: Matplotlib axes to render on. If None, creates new figure.
        """
        raise NotImplementedError("Render method must be implemented by subclasses")
