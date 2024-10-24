import random

def create_deck():
    # Return a standard deck of 52 cards
    ranks = "23456789TJQKA"
    suits = "HDCS"
    return [(rank, suit) for rank in ranks for suit in suits]


def shuffle_deck(deck):
    # Shuffle the provided deck
    random.shuffle(deck)
    return deck

# Unicode symbols for suits
SUIT_SYMBOLS = {
    'H': '♥',
    'D': '♦',
    'C': '♣',
    'S': '♠',
}

def deal_cards(deck, num_players=2):
    # Deal cards for a Texas hold'em game
    # Ensure we can deal cards to the number of players plus the community cards
    if len(deck) < num_players * 2 + 5:
        raise ValueError("Not enough cards in the deck to deal")

    # Deal 2 cards to each player
    player_hands = [deck[i*2:i*2+2] for i in range(num_players)]

    # Deal 5 community cards
    community_cards = deck[num_players*2:num_players*2+5]

    return player_hands, community_cards


def parse_card(card_str):
    # Error checking
    if len(card_str) != 2 or card_str[0] not in "23456789TJQKA" or card_str[1] not in "HDCS":
        raise ValueError(f"{card_str} is not a valid card representation.")

    # Convert a two-character string into a card representation
    rank = card_str[0]
    suit = card_str[1]
    return (rank, suit)


def parse_hand(hand_str):
    # Convert a string of cards into a list of card representations
    cards = hand_str.split()
    return [parse_card(card) for card in cards]

# Pretty print a single card using Unicode symbols
def pretty_print_card(card):
    rank, suit = card
    return f"{rank}{SUIT_SYMBOLS[suit]}"

# Pretty print an entire hand (list of cards)
def pretty_print_hand(hand):
    return ' '.join(pretty_print_card(card) for card in hand)