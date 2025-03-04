"""Utility for managing image indices for cards."""
from typing import Dict

# Global image index tracker
_image_indices: Dict[str, int] = {
    'farm': 0, 'industrial': 0, 'residential': 0,'sell_market': 0, 'buy_market': 0, 'process': 0, 'hq': 0
}

def get_next_image_index(card_type: str) -> int:
    """Get and increment the image index for a card type.
    
    Args:
        card_type: The type of card to get index for
        
    Returns:
        int: The current index before incrementing
        
    Raises:
        ValueError: If card_type is not valid
    """
    if card_type not in _image_indices:
        raise ValueError(f"Invalid card type: {card_type}")
        
    current_idx = _image_indices[card_type]
    _image_indices[card_type] += 1
    return current_idx

def reset_image_indices() -> None:
    """Reset all image indices to 0."""
    for key in _image_indices:
        _image_indices[key] = 0
