"""Deck model for managing collections of cards."""
from typing import List, Optional
import random
import matplotlib.pyplot as plt
from .card import Card

class Deck:
    """A deck of cards that can be manipulated and rendered."""
    
    def __init__(self, cards: List[Card]) -> None:
        """Initialize a deck with a list of cards.
        
        Args:
            cards: List of Card objects to initialize the deck with
        """
        self.cards = cards
 
    def render(self) -> None:
        """Render all cards in the deck in a horizontal layout."""
        fig, axs = plt.subplots(1, len(self.cards))
        fig.set_figwidth(12)
        fig.set_figheight(3)
        
        for i, card in enumerate(self.cards):
            if card is not None:
                card.render(ax=axs[i])

    def remove_cards(self, cards: List[Card]) -> None:
        """Remove specified cards from the deck.
        
        Args:
            cards: List of cards to remove
        """
        for card in cards:
            self.cards.remove(card)

    def take_N_random(self, N: int) -> List[Card]:
        """Take N random cards from the deck.
        
        Args:
            N: Number of cards to take
            
        Returns:
            List of randomly selected cards
        """
        res = []
        for _ in range(N):
            x = random.choice(self.cards)
            self.cards.remove(x)
            res.append(x)
        return res

    def take_N_from_bottom(self, N: int) -> List[Card]:
        """Take N cards from the bottom of the deck.
        
        Args:
            N: Number of cards to take
            
        Returns:
            List of cards from the bottom
        """
        res = self.cards[0:N]
        self.cards = self.cards[N:]
        return res

    def take_N_from_top(self, N: int) -> List[Card]:
        """Take N cards from the top of the deck.
        
        Args:
            N: Number of cards to take
            
        Returns:
            List of cards from the top
        """
        res = self.cards[-N:]
        self.cards = self.cards[:-N]
        return res

    def add_N_to_bottom(self, cards: List[Card]) -> None:
        """Add cards to the bottom of the deck.
        
        Args:
            cards: List of cards to add
        """
        self.cards = cards + self.cards
   
    def add_N_to_top(self, cards: List[Card]) -> None:
        """Add cards to the top of the deck.
        
        Args:
            cards: List of cards to add
        """
        self.cards.extend(cards)
    
    def shuffle(self) -> List[Card]:
        """Shuffle the deck.
        
        Returns:
            The shuffled list of cards
        """
        random.shuffle(self.cards)
        return self.cards
