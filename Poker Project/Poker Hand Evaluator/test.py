import pytest
from card_utils import deal_cards
from poker_logic import (
    best_hand,
    hand_name, is_flush, is_straight, hand_value, compare_hands,
    HIGH_CARD, ROYAL_FLUSH, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND,
    STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND, STRAIGHT_FLUSH
)

# 1. Testing utility functions
def test_hand_name():
    assert hand_name(HIGH_CARD) == "High Card"
    assert hand_name(ROYAL_FLUSH) == "Royal Flush"
    assert hand_name(10) == "Unknown Hand" # Some random number out of range

def test_is_flush():
    assert is_flush([('2', 'S'), ('4', 'S'), ('7', 'S'), ('9', 'S'), ('Q', 'S')])
    assert not is_flush([('2', 'S'), ('4', 'H'), ('7', 'S'), ('9', 'S'), ('Q', 'S')])

def test_is_straight():
    assert is_straight([('2', 'S'), ('3', 'H'), ('4', 'D'), ('5', 'C'), ('6', 'H')])
    assert not is_straight([('2', 'S'), ('3', 'H'), ('5', 'D'), ('6', 'C'), ('7', 'H')])


# 2. Testing hand value for different hand types
def test_hand_value_high_card():
    hand = [('2', 'S'), ('4', 'H'), ('7', 'D'), ('9', 'C'), ('Q', 'H')]
    assert hand_value(hand) == (HIGH_CARD, ['Q'], ['9', '7', '4', '2'])

def test_hand_value_one_pair():
    hand = [('2', 'S'), ('2', 'H'), ('7', 'D'), ('9', 'C'), ('Q', 'H')]
    assert hand_value(hand) == (ONE_PAIR, ['2'], ['Q', '9', '7'])

def test_hand_value_two_pair():
    hand = [('2', 'S'), ('2', 'H'), ('7', 'D'), ('7', 'C'), ('Q', 'H')]
    assert hand_value(hand) == (TWO_PAIR, ['7', '2'], ['Q'])

def test_hand_value_three_of_a_kind():
    hand = [('2', 'S'), ('2', 'H'), ('2', 'D'), ('7', 'C'), ('Q', 'H')]
    assert hand_value(hand) == (THREE_OF_A_KIND, ['2'], ['Q', '7'])

def test_hand_value_straight():
    hand = [('3', 'S'), ('4', 'H'), ('5', 'D'), ('6', 'C'), ('7', 'H')]
    assert hand_value(hand) == (STRAIGHT, ['7'], [])

def test_hand_value_flush():
    hand = [('2', 'S'), ('4', 'S'), ('7', 'S'), ('9', 'S'), ('Q', 'S')]
    assert hand_value(hand) == (FLUSH, ['Q', '9', '7', '4', '2'], [])

def test_hand_value_full_house():
    hand = [('2', 'S'), ('2', 'H'), ('7', 'D'), ('7', 'C'), ('7', 'H')]
    assert hand_value(hand) == (FULL_HOUSE, ['7'], ['2'])

def test_hand_value_four_of_a_kind():
    hand = [('2', 'S'), ('2', 'H'), ('2', 'D'), ('2', 'C'), ('Q', 'H')]
    assert hand_value(hand) == (FOUR_OF_A_KIND, ['2'], ['Q'])

def test_hand_value_straight_flush():
    hand = [('3', 'S'), ('4', 'S'), ('5', 'S'), ('6', 'S'), ('7', 'S')]
    assert hand_value(hand) == (STRAIGHT_FLUSH, ['7'], [])

def test_hand_value_royal_flush():
    hand = [('T', 'S'), ('J', 'S'), ('Q', 'S'), ('K', 'S'), ('A', 'S')]
    assert hand_value(hand) == (ROYAL_FLUSH, ['A'], [])

# 3. Testing game scenarios
def test_straight_flush():
    player_cards = [('5', 'C'), ('6', 'C')]
    community_cards = [('7', 'C'), ('8', 'C'), ('9', 'C'), ('2', 'H'), ('3', 'D')]
    hand_rank, _, _ = best_hand(player_cards, community_cards)
    assert hand_rank == STRAIGHT_FLUSH


def test_best_hand():
    player_cards = [('2', 'S'), ('4', 'H')]
    community_cards = [('3', 'D'), ('5', 'C'), ('6', 'H'), ('7', 'S'), ('8', 'D')]
    assert best_hand(player_cards, community_cards) == (STRAIGHT, ['8'], [])  # It forms a straight

def test_compare_hands():
    hand1 = [('2', 'S'), ('4', 'H'), ('7', 'D'), ('9', 'C'), ('Q', 'H')]
    hand2 = [('2', 'S'), ('4', 'H'), ('7', 'D'), ('9', 'C'), ('K', 'H')]
    assert compare_hands(hand1, hand2) == -1 # Since hand2 has a King high vs hand1's Queen high

def test():
    test_cases = [
        (["TS", "JS", "QS", "KS", "AS"], (ROYAL_FLUSH, ["A"], [])), # Straight flush with Ace high
        (["AS", "2S", "3S", "4S", "5S"], (STRAIGHT_FLUSH, ['5'], [])), # Straight flush with Ace low
        (["4S", "4D", "4C", "TS", "AS"], (THREE_OF_A_KIND, ['4'], ['A', 'T'])), # Three of a kind with correct kickers
        (["TS", "TD", "JS", "JD", "3S"], (TWO_PAIR, ['J', 'T'], ['3'])), # Two pairs
        (["TS", "TD", "JS", "QD", "KS"], (ONE_PAIR, ['T'], ['K', 'Q', 'J'])), # One pair
        (["4S", "4D", "4C", "4H", "AS"], (FOUR_OF_A_KIND, ['4'], ['A'])),  # Four of a Kind with Ace kicker
        (["2S", "6S", "8S", "JS", "QS"], (FLUSH, ['Q', 'J', '8', '6', '2'], [])),  # Flush
        (["7H", "8D", "9S", "TH", "JS"], (STRAIGHT, ['J'], [])),  # Straight with J high
        (["2C", "4D", "6S", "9H", "KC"], (HIGH_CARD, ['K'], ['9', '6', '4', '2'])),  # High Card with K high
        (["2H", "2D", "2S", "3C", "3S"], (FULL_HOUSE, ['2'], ['3'])),  # Full House with 2s over 3s
        (["JS", "JD", "JC", "AH", "KH"], (THREE_OF_A_KIND, ['J'], ['A', 'K'])),  # Three of a kind with A and K as kickers
        (["4S", "4D", "6H", "6C", "AS"], (TWO_PAIR, ['6', '4'], ['A'])),  # Two pairs with Ace kicker
        (["8S", "8D", "3S", "6H", "KC"], (ONE_PAIR, ['8'], ['K', '6', '3'])),  # One pair with K, 6, 3 as kickers
        (["TH", "JS", "QS", "KH", "AS"], (STRAIGHT, ['A'], [])),  # Straight with Ace high
        (["2S", "3C", "4D", "5H", "7C"], (HIGH_CARD, ['7'], ['5', '4', '3', '2'])),  # High Card with 7 high
        (["2S", "4S", "6S", "8S", "TS"], (FLUSH, ['T', '8', '6', '4', '2'], [])), # Regular flush
        (["2S", "3D", "4H", "5S", "6C"], (STRAIGHT, ['6'], [])), # Regular straight
        (["TS", "TD", "TH", "3S", "2D"], (THREE_OF_A_KIND, ['T'], ['3', '2'])), # Three of a kind, unordered kickers
        (["2S", "2D", "4S", "4D", "6H"], (TWO_PAIR, ['4', '2'], ['6'])), # Two pairs unordered
        (["2S", "4S", "6S", "8S", "TC"], (HIGH_CARD, ['T'], ['8', '6', '4', '2'])), # One card from flush
        (["2S", "3D", "4H", "5S", "7C"], (HIGH_CARD, ['7'], ['5', '4', '3', '2'])), # One card from straight
        (["2S", "3S", "4S", "5S", "7C"], (HIGH_CARD, ['7'], ['5', '4', '3', '2'])), # One card from both flush and straight
        (["2S", "2D", "2H", "3S", "3D"], (FULL_HOUSE, ['2'], ['3'])), # Full house 2 over 3
        (["TS", "4D", "4S", "4H", "4C"], (FOUR_OF_A_KIND, ['4'], ['T'])), # Four of a kind unordered
        (["2S", "2H", "2D", "2C", "AS"], (FOUR_OF_A_KIND, ['2'], ['A'])), # Four of a kind with kicker
        (["2S", "4S", "6S", "8S", "JS"], (FLUSH, ['J', '8', '6', '4', '2'], [])), # Flush with mixed cards
        (["3H", "4H", "5C", "2D", "AS"], (STRAIGHT, ['5'], [])), # Low-end straight with mixed suits
        (["TS", "TD", "TH", "TC", "2D"], (FOUR_OF_A_KIND, ['T'], ['2'])),  # Four of a Kind with 'T's and a '2' kicker
        (["7S", "9D", "JH", "3S", "2D"], (HIGH_CARD, ['J'], ['9', '7', '3', '2'])), # High card with no ace
        (["2S", "2D", "3H", "4C", "5S"], (ONE_PAIR, ['2'], ['5', '4', '3'])), # Low-end pair
        (["2H", "3H", "4H", "5H", "6H"], (STRAIGHT_FLUSH, ['6'], [])), # Straight flush with mixed ranks
        (["2S", "4S", "6S", "8S", "TS"], (FLUSH, ['T', '8', '6', '4', '2'], [])), # Flush with gaps
        (["AS", "JC", "9D", "5H", "3S"], (HIGH_CARD, ['A'], ['J', '9', '5', '3'])), # All kickers unordered
        (["AS", "2H", "3D", "4C", "5S"], (STRAIGHT, ['5'], [])), # Ace low straight
        (["AS", "AD", "AH", "2S", "2D"], (FULL_HOUSE, ['A'], ['2'])), # Full House Aces over Twos
        (["AS", "KC", "QD", "JH", "TS"], (STRAIGHT, ['A'], [])),  # Straight from Ten to Ace
        (["2S", "2H", "2D", "2C", "3S"], (FOUR_OF_A_KIND, ['2'], ['3'])),  # Four of a Kind of 2s with a '3' kicker
        (["2S", "3S", "4S", "5S", "7D"], (HIGH_CARD, ['7'], ['5', '4', '3', '2'])), # One card from straight flush
        (["2S", "3S", "4S", "5D", "6H"], (STRAIGHT, ['6'], [])),  # Straight with 6 high
        (["TS", "JS", "QS", "KS", "9H"], (STRAIGHT, ['K'], [])),  # Straight with King high
        (["2H", "3H", "4H", "5H", "7H"], (FLUSH, ['7', '5', '4', '3', '2'], [])), # One card from straight flush with mixed ranks
        (["6S", "6D", "4S", "4H", "AS"], (TWO_PAIR, ['6', '4'], ['A'])),  # Two pairs with Ace kicker
        (["6S", "6D", "4S", "4H", "TS"], (TWO_PAIR, ['6', '4'], ['T'])),  # Two pairs with Ten kicker
        (["AS", "2D", "3S", "4C", "5H"], (STRAIGHT, ['5'], [])),  # Ace low straight
        (["AS", "2D", "3S", "4C", "6H"], (HIGH_CARD, ['A'], ['6', '4', '3', '2'])),  # High card with Ace
        (["5H", "3H", "4H", "2H", "6H"], (STRAIGHT_FLUSH, ['6'], [])), # Straight flush out of order
        (["AS", "AD", "3H", "4C", "5S"], (ONE_PAIR, ['A'], ['5', '4', '3'])),  # One pair of Aces with high kickers
    ]

    for hand, expected in test_cases:
        result = hand_value(hand)
        assert result == expected, f"Expected {expected} but got {result} for hand {hand}."
    print("All tests passed!")

test()