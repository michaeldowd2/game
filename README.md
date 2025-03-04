# Business Strategy Board Game Concept

A competitive business simulation board game concept, programmed in python for balancing and configuration game parameters. Players compete to build and manage the most profitable company through strategic placement of buildings, employee management, and market operations.

## Features

- Dynamic board generation with multiple layout styles (rectangle, diamond, linear)
- Players 2 - 4
- Various building types:
  - Buy Markets: Purchase resources at competitive prices
  - Processing Plants: Convert resources into products
  - Sell Markets: Sell products to maximize profits
  - Headquarters: Manage operations and employees
- Visual game state representation basic ai for balancing game parameters

## Installation

1. Clone the repository:
```bash
git clone https://github.com/michaeldowd2/game.git
cd game
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

```python
from models import Game, Settings

# Initialize game with default settings
settings = Settings()
game = Game(settings, no_players=2, board_style='rectangle')

# View the game board
print(game.board)

# Calculate player's net worth
net_worth = game.board.calc_player_net(0)
print(f"Player 0 net worth: {net_worth}")
```

### Board Styles

The game supports three board layouts:
- `rectangle`: Traditional grid layout
- `diamond`: Diamond-shaped board
- `linear`: Linear arrangement of spaces

### Building Types

1. **Buy Market** (`buy_market`)
   - Purchase resources
   - Value based on total market spend and player spend

2. **Sell Market** (`sell_market`)
   - Sell finished products
   - Value based on total market price and player price

3. **Processing Plant** (`process`)
   - Convert resources into products
   - Value based on connected buy and sell markets

4. **Headquarters** (`hq`)
   - Manage operations
   - Controls employee and building limits

## Development

### Running Tests

```bash
python -m unittest tests/test_game.py -v
```

### Project Structure

```
game/
├── assets/          # Game assets and themes
├── config/          # Configuration files
├── models/          # Core game components
│   ├── board.py
│   ├── card.py
│   ├── deck.py
│   ├── game.py
│   ├── player.py
│   └── settings.py
├── tests/           # Test suite
├── utils/           # Utility functions
└── requirements.txt # Project dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
