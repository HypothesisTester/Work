# README.md for Texas Hold’em Hand Evaluator

## Introduction:
This project is a Poker Game Simulator designed to emulate the fundamental mechanics of a Texas hold'em game. The objective of the simulator is not only to deal and compare cards but to ensure that the game logic and rules are maintained with precision. The project is organized into three main operational files and a comprehensive testing suite.

## Operational Files:

### 1. `card_utils.py`
This file consists of utility functions that assist in manipulating and representing cards:
- `create_deck()`: Returns a standard deck of 52 cards.
- `shuffle_deck(deck)`: Accepts a deck and shuffles it to ensure randomness.
- `deal_cards(deck, num_players=2)`: Deals cards to the specified number of players, including the community cards.
- `parse_card(card_str)`: Converts a two-character string (like "KH" for King of Hearts) into a card representation. It also checks for validity.
- `parse_hand(hand_str)`: Converts a string of cards into a list of card representations.
- `pretty_print_card(card)`: Prints a single card using Unicode symbols.
- `pretty_print_hand(hand)`: Prints an entire hand in a visually appealing manner.

### 2. `poker_logic.py`
This file enforces the core game rules and mechanics:
- `hand_name(rank)`: Returns a human-readable string representation of a hand rank.
- `hand_value(hand)`: Evaluates the value of a hand.
- `is_flush(hand)`: Checks if a hand is a flush.
- `is_straight(hand)`: Checks if a hand is a straight. Contains special handling for an Ace.
- `best_hand(player_cards, community_cards)`: Determines the best hand combination.
- `compare_hands(hand1, hand2)`: Compares two poker hands and returns the winner.

### 3. `project.py`
This file is the main entry point for the simulator:
- `main()`: Manages the game loop, player inputs, and facilitates game rounds.
- `simulate_round(num_players=2)`: Simulates a game round, handles the card dealing, and determines the winner.

## Testing Suite: `test.py`
This is a comprehensive test suite designed to ensure the functionality and reliability of the game logic:

- **Utility Functions Testing**:
  - `test_hand_name()`
  - `test_is_flush()`
  - `test_is_straight()`

- **Hand Value Testing**:
  - `test_hand_value_high_card()`
  - `test_hand_value_one_pair()`
  - `test_hand_value_two_pair()`
  - `test_hand_value_three_of_a_kind()`
  - `test_hand_value_straight()`
  - `test_hand_value_flush()`
  - `test_hand_value_full_house()`
  - `test_hand_value_four_of_a_kind()`
  - `test_hand_value_straight_flush()`

- **Game Scenarios Testing**:
  - `test_straight_flush()`
  - `test_best_hand()`
  - `test_compare_hands()`
  - `test()`: A comprehensive test function which checks against 46    different test cases.

  ## Design Choices & Reflections:

- **Project Structure**:
  - **Initial Assumption**:  At the outset, it seemed a singular file might suffice. However, as the project grew in complexity, the need for organisation became evident.
  - **Outcome**: The project was organised into distinct files, enhancing clarity and facilitating potential extensions. The addition of `test.py` ensured the system's functionality and robustness were consistently verified.

- **Function Design & Documentation**:
  - **Objective**: Each function was designed to serve a specific role, ensuring code efficiency and maintainability.
  - **Commenting Approach**: Concise comments were incorporated with each function to provide a brief overview and purpose.

- **Provision for Future Enhancements**:
  - **Vision**: Beyond the core function of hand evaluation, the project was structured with the foresight to accommodate potential features, such as betting rounds or opponent AI mechanics.

- **Iterative Development & Quality Assurance**:
  - **Initial Limitations**: The primary version of `poker_logic.py` was foundational and overlooked certain edge cases.
  - **Refinement**: The comprehensive tests provided by `test.py` allowed for systematic improvements, ensuring comprehensive coverage and reliable performance.