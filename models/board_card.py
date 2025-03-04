"""Board card model for game board spaces."""
from typing import Optional
from .card import Card

class BoardCard(Card):
    """A card representing a space on the game board."""
    
    def __init__(self, name: str = '', card_type: str = '', max_employees: int = 3) -> None:
        """Initialize a board card.
        
        Args:
            name: Name of the board space
            card_type: Type of board space
            max_employees: Maximum number of employees allowed on this space
        """
        super().__init__(name, card_type)
        self.max_employees = max_employees

    def __str__(self) -> str:
        """String representation of the board card.
        
        Returns:
            Formatted string with card details
        """
        if self.card_type == 'farm':
            return self.colour('F' + str(self.max_employees), 'green')
        elif self.card_type == 'residential':
            return self.colour('R' + str(self.max_employees), 'red')
        elif self.card_type == 'industry':
            return self.colour('I' + str(self.max_employees), 'yellow')
        else:
            return '-' + str(self.max_employees)

    def colour(self, s: str, colour: str = '') -> str:
        """String representation of the board card.
        
        Returns:
            Formatted string with card details
        """
        if colour == 'blue':
            return "\x1b[34m" + s + "\x1b[0m"
        elif colour == 'yellow':
            return "\x1b[33m" + s + "\x1b[0m"
        elif colour == 'green':
            return "\x1b[32m" + s + "\x1b[0m"
        elif colour == 'red':
            return "\x1b[31m" + s + "\x1b[0m"
        else:
            return s
