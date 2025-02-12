# poker_game.py

import random
import logging
from itertools import combinations

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Unicode symbols for suits
SUIT_SYMBOLS = {
    'H': '♥',
    'D': '♦',
    'C': '♣',
    'S': '♠',
}

# Card value mappings
RANK_VALUES = {rank: index for index, rank in enumerate("23456789TJQKA", start=2)}

# Hand ranks
(
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    ROYAL_FLUSH,
) = range(10)

# Custom Exception Classes
class InsufficientChipsError(Exception):
    """Raised when a player does not have enough chips for a bet or call."""
    pass

class InvalidActionError(Exception):
    """Raised when an invalid action is attempted."""
    pass

# Helper functions for cards
def create_deck():
    # Return a standard deck of 52 cards
    ranks = "23456789TJQKA"
    suits = "HDCS"
    return [(rank, suit) for rank in ranks for suit in suits]

def shuffle_deck(deck):
    # Shuffle the provided deck
    random.shuffle(deck)
    return deck

def pretty_print_card(card):
    rank, suit = card
    return f"{rank}{SUIT_SYMBOLS[suit]}"

def pretty_print_hand(hand):
    return ' '.join(pretty_print_card(card) for card in hand)

# Poker logic functions
def hand_name(rank):
    # Return a human-readable string representation of a hand rank
    rank_names = {
        HIGH_CARD: "High Card",
        ONE_PAIR: "One Pair",
        TWO_PAIR: "Two Pair",
        THREE_OF_A_KIND: "Three of a Kind",
        STRAIGHT: "Straight",
        FLUSH: "Flush",
        FULL_HOUSE: "Full House",
        FOUR_OF_A_KIND: "Four of a Kind",
        STRAIGHT_FLUSH: "Straight Flush",
        ROYAL_FLUSH: "Royal Flush",
    }
    return rank_names.get(rank, "Unknown Hand")

def hand_value(hand):
    rank_counts = {}
    for rank in RANK_VALUES.keys():
        rank_counts[rank] = 0
    for card in hand:
        rank_counts[card[0]] += 1
    rank_counts = sorted(rank_counts.items(), key=lambda x: (x[1], RANK_VALUES[x[0]]), reverse=True)

    four = [rank for rank, count in rank_counts if count == 4]
    if four:
        kicker = [rank for rank, count in rank_counts if count == 1]
        return (FOUR_OF_A_KIND, four, kicker)

    three = [rank for rank, count in rank_counts if count == 3]
    two = [rank for rank, count in rank_counts if count == 2]

    if three and two:
        return (FULL_HOUSE, three, two)

    if is_flush(hand) and is_straight(hand):
        values = sorted(RANK_VALUES[card[0]] for card in hand)
        if values == [10, 11, 12, 13, 14]:
            return (ROYAL_FLUSH, ['A'], [])
        elif values == [2, 3, 4, 5, 14]:
            return (STRAIGHT_FLUSH, ['5'], [])
        else:
            high_card = sorted(hand, key=lambda card: RANK_VALUES[card[0]])[-1][0]
            return (STRAIGHT_FLUSH, [high_card], [])

    if is_flush(hand):
        ranks = sorted((card[0] for card in hand), key=lambda x: RANK_VALUES[x], reverse=True)
        return (FLUSH, ranks, [])

    if is_straight(hand):
        values = sorted(RANK_VALUES[card[0]] for card in hand)
        if values == [2, 3, 4, 5, 14]:
            return (STRAIGHT, ['5'], [])
        high_card = sorted(hand, key=lambda card: RANK_VALUES[card[0]])[-1][0]
        return (STRAIGHT, [high_card], [])

    if three:
        kicker_ranks = [rank for rank, count in rank_counts if count == 1]
        kicker = sorted(kicker_ranks, key=lambda x: RANK_VALUES[x], reverse=True)[:2]
        return (THREE_OF_A_KIND, three, kicker)

    if len(two) == 2:
        one_pair_kicker = [rank for rank, count in rank_counts if count == 1]
        return (TWO_PAIR, two, one_pair_kicker)

    if len(two) == 1:
        one_pair_kicker = sorted(
            [rank for rank, count in rank_counts if count == 1], key=lambda x: RANK_VALUES[x], reverse=True
        )
        return (ONE_PAIR, two, one_pair_kicker)

    kicker = sorted((card[0] for card in hand), key=lambda x: RANK_VALUES[x], reverse=True)
    return (HIGH_CARD, [kicker[0]], kicker[1:])

def is_flush(hand):
    suits = [s for _, s in hand]
    return len(set(suits)) == 1

def is_straight(hand):
    values = sorted(RANK_VALUES[card[0]] for card in hand)
    if values[-1] - values[0] == 4 and len(set(values)) == 5:
        return True
    # Special case for Ace as high and low in straight
    if values == [2, 3, 4, 5, 14]:
        return True
    return False

def best_hand(player_cards, community_cards):
    all_cards = player_cards + community_cards
    best_rank = (-1, [], [])
    # Compare hands based on the primary and secondary evaluation metrics
    for combo in combinations(all_cards, 5):
        current_value = hand_value(sorted(combo, key=lambda card: RANK_VALUES[card[0]]))

        if current_value > best_rank:
            best_rank = current_value

    return best_rank

# PlayerStats class
class PlayerStats:
    def __init__(self):
        self.game_history = []
        self.wins = 0
        self.losses = 0
        self.total_hands_played = 0
        self.aggressive_actions = 0
        self.fold_count = 0
        self.showdown_count = 0
        self.preflop_raise_count = 0
        self.vpip_actions = 0
        self.postflop_bets = 0
        self.postflop_raises = 0
        self.postflop_calls = 0
        self.total_pot_contributions = 0
        self.contribution_count = 0

    def update_game_result(self, result):
        self.total_hands_played += 1
        self.game_history.append(result)
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1

    def update_aggressive_action(self):
        self.aggressive_actions += 1

    def update_fold(self):
        self.fold_count += 1

    def update_showdown(self):
        self.showdown_count += 1

    def update_preflop_raise(self):
        self.preflop_raise_count += 1

    def update_vpip_action(self):
        self.vpip_actions += 1

    def update_postflop_action(self, action_type):
        if action_type == 'bet':
            self.postflop_bets += 1
        elif action_type == 'raise':
            self.postflop_raises += 1
        elif action_type == 'call':
            self.postflop_calls += 1

    def update_pot_contribution(self, amount):
        self.total_pot_contributions += amount
        self.contribution_count += 1

    def get_postflop_aggression_factor(self):
        if self.postflop_calls == 0:
            return 0
        return (self.postflop_bets + self.postflop_raises) / self.postflop_calls

    def get_average_pot_contribution(self):
        if self.contribution_count == 0:
            return 0
        return self.total_pot_contributions / self.contribution_count

    def get_win_percentage(self):
        if self.total_hands_played == 0:
            return 0
        return (self.wins / self.total_hands_played) * 100

# Player class
class Player:
    def __init__(self, name, chip_count, position, stats):
        self.name = name
        self.chip_count = chip_count
        self.hand = []
        self.position = position
        self.current_bet = 0
        self.total_pot_contribution = 0
        self.is_folded = False
        self.is_all_in = False
        self.stats = stats
        self.decision_maker = DecisionMaker(self)

    def add_chips(self, amount):
        self.chip_count += amount

    def fold(self):
        self.is_folded = True
        self.hand = []
        self.stats.update_fold()  # Updating fold count

    def bet(self, amount):
        if amount < 0:
            raise ValueError("Bet amount cannot be negative.")
        if amount > self.chip_count:
            amount = self.chip_count
            self.is_all_in = True
        self.chip_count -= amount
        self.current_bet += amount
        self.total_pot_contribution += amount
        self.stats.update_aggressive_action()  # Aggressive action
        self.stats.update_vpip_action()  # VPIP action
        self.stats.update_pot_contribution(amount)  # Pot contribution

    def check(self):
        pass

    def call(self, current_highest_bet):
        bet_amount = current_highest_bet - self.current_bet
        if bet_amount > self.chip_count:
            bet_amount = self.chip_count
            self.is_all_in = True
        self.chip_count -= bet_amount
        self.current_bet += bet_amount
        self.total_pot_contribution += bet_amount
        self.stats.update_pot_contribution(bet_amount)  # Pot contribution

    def raise_bet(self, raise_amount, current_highest_bet):
        total_bet = current_highest_bet + raise_amount
        bet_increment = total_bet - self.current_bet
        if bet_increment > self.chip_count:
            total_bet = self.current_bet + self.chip_count
            self.is_all_in = True
            bet_increment = self.chip_count
        self.chip_count -= bet_increment
        self.current_bet += bet_increment
        self.total_pot_contribution += bet_increment
        self.stats.update_aggressive_action()  # Aggressive action
        self.stats.update_vpip_action()  # VPIP action
        self.stats.update_pot_contribution(bet_increment)  # Pot contribution

    def receive_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return self.hand

    def display_status(self):
        return f"{self.name} - Chips: {self.chip_count}, Bet: {self.current_bet}, Hand: {'Folded' if self.is_folded else pretty_print_hand(self.hand)}"

    def reset_for_new_round(self):
        """Reset the player's state for a new round."""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.total_pot_contribution = 0

    def log_action(self, action, amount=None):
        action_detail = f"{action}{' ' + str(amount) if amount is not None else ''}"
        logging.info(f"Player {self.position} ({self.name}): {action_detail}")

# DecisionMaker class
class DecisionMaker:
    def __init__(self, player):
        self.player = player

    def get_action(self, game_state):
        # For simplicity, we'll get input from the console
        print(f"\n{self.player.name}'s turn. Available actions: 'fold', 'check', 'call', 'bet', 'raise'")
        while True:
            action = input("Enter your action: ").lower()
            if action in ['fold', 'check', 'call', 'bet', 'raise']:
                return action
            else:
                print("Invalid action. Please choose from 'fold', 'check', 'call', 'bet', 'raise'.")

    def get_bet_amount(self, min_bet=0):
        while True:
            try:
                amount = int(input(f"Enter bet amount (minimum {min_bet}): "))
                if amount >= min_bet and amount <= self.player.chip_count:
                    return amount
                else:
                    print(f"Invalid amount. Please bet an amount between {min_bet} and your chip count ({self.player.chip_count}).")
            except ValueError:
                print("Please enter a valid number.")

    def get_raise_amount(self, min_raise):
        while True:
            try:
                amount = int(input(f"Enter raise amount (minimum {min_raise}): "))
                if amount >= min_raise and amount <= self.player.chip_count:
                    return amount
                else:
                    print(f"Invalid amount. Please ensure you have enough chips to raise at least {min_raise} and up to your chip count ({self.player.chip_count}).")
            except ValueError:
                print("Please enter a valid number.")

# Game class
class Game:
    def __init__(self, players):
        self.players = players
        self.small_blind = 10  # Set as per game rules
        self.big_blind = 20    # Set as per game rules
        self.dealer_position = 0
        self.current_round = "pre-flop"
        self.community_cards = []
        self.pot = 0
        self.deck = []
        self.current_highest_bet = 0

    def start_game(self):
        while True:
            self.play_round()
            # Check if any player has run out of chips
            active_players = [player for player in self.players if player.chip_count > 0]
            if len(active_players) < 2:
                print("Game over. Not enough players to continue.")
                break
            play_again = input("Play another round? (yes/no): ").lower()
            if play_again in ["no", "n"]:
                print("Thanks for playing!")
                break
            self.prepare_next_round()

    def prepare_next_round(self):
        # Reset game state and advance dealer position
        self.reset_game()
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

    def play_round(self):
        self.deck = shuffle_deck(create_deck())
        self.current_highest_bet = 0
        self.deal_cards()
        self.post_blinds()
        self.play_betting_round(starting_player=(self.dealer_position + 3) % len(self.players))
        self.current_round = "flop"
        self.deal_community_cards(3)
        self.play_betting_round(starting_player=(self.dealer_position + 1) % len(self.players))
        self.current_round = "turn"
        self.deal_community_cards(1)
        self.play_betting_round(starting_player=(self.dealer_position + 1) % len(self.players))
        self.current_round = "river"
        self.deal_community_cards(1)
        self.play_betting_round(starting_player=(self.dealer_position + 1) % len(self.players))
        self.end_game()

    def deal_cards(self):
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.pop())
        print("\nPlayers' Hands:")
        for player in self.players:
            print(f"{player.name}'s hand: {pretty_print_hand(player.hand)}")

    def deal_community_cards(self, number):
        # Burn a card before dealing community cards
        self.deck.pop()
        for _ in range(number):
            self.community_cards.append(self.deck.pop())
        print(f"\nCommunity Cards ({self.current_round}): {pretty_print_hand(self.community_cards)}")

    def post_blinds(self):
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]
        print(f"\nPosting blinds:")
        print(f"{small_blind_player.name} posts small blind of {self.small_blind}")
        small_blind_player.bet(self.small_blind)
        self.pot += self.small_blind
        print(f"{big_blind_player.name} posts big blind of {self.big_blind}")
        big_blind_player.bet(self.big_blind)
        self.pot += self.big_blind
        self.current_highest_bet = self.big_blind

    def play_betting_round(self, starting_player):
        active_players = [player for player in self.players if not player.is_folded and not player.is_all_in]
        players_in_round = active_players.copy()
        betting_complete = False
        while not betting_complete:
            betting_complete = True
            for i in range(len(self.players)):
                player_index = (starting_player + i) % len(self.players)
                player = self.players[player_index]
                if player.is_folded or player.is_all_in:
                    continue
                print(f"\nCurrent Pot: {self.pot}")
                print(player.display_status())
                print(f"Current highest bet: {self.current_highest_bet}")
                action = player.decision_maker.get_action(self)
                if action == 'fold':
                    player.fold()
                    players_in_round.remove(player)
                    # If only one player remains, they win the pot
                    if len(players_in_round) == 1:
                        self.end_game()
                        return
                elif action == 'check':
                    if player.current_bet < self.current_highest_bet:
                        print("You cannot check when there is a bet. You must call or raise.")
                        betting_complete = False
                        continue
                elif action == 'call':
                    call_amount = self.current_highest_bet - player.current_bet
                    player.call(self.current_highest_bet)
                    self.pot += call_amount
                    if player.is_all_in:
                        print(f"{player.name} is all-in!")
                elif action == 'bet':
                    min_bet = max(self.big_blind, self.current_highest_bet)
                    bet_amount = player.decision_maker.get_bet_amount(min_bet)
                    self.current_highest_bet = bet_amount
                    player.bet(bet_amount)
                    self.pot += bet_amount
                    betting_complete = False
                elif action == 'raise':
                    min_raise = self.big_blind
                    raise_amount = player.decision_maker.get_raise_amount(min_raise)
                    player.raise_bet(raise_amount, self.current_highest_bet)
                    self.current_highest_bet = player.current_bet
                    self.pot += (player.current_bet - self.current_highest_bet)
                    betting_complete = False
                else:
                    print("Invalid action.")
                player.log_action(action, player.current_bet)
            # Check if all active players have matched the highest bet
            active_players = [player for player in self.players if not player.is_folded and not player.is_all_in]
            if any(player.current_bet < self.current_highest_bet for player in active_players):
                betting_complete = False
            else:
                betting_complete = True

    def end_game(self):
        # Hand Evaluation
        active_players = [player for player in self.players if not player.is_folded]
        if not active_players:
            print("All players have folded. No winner.")
            return

        best_hands = {}
        for player in active_players:
            best_hands[player] = best_hand(player.hand, self.community_cards)
            print(f"{player.name}'s best hand: {hand_name(best_hands[player][0])}")

        # Determine the winner
        winning_hand_value = max(best_hands.values(), key=lambda x: (x[0], x[1], x[2]))
        winners = [player for player, hand in best_hands.items() if hand == winning_hand_value]

        # Distribute pot
        pot_share = self.pot // len(winners)
        for winner in winners:
            winner.chip_count += pot_share
            print(f"{winner.name} wins {pot_share} chips with a {hand_name(winning_hand_value[0])}!")
            winner.stats.update_game_result("win")
        # Update losers' stats
        for player in self.players:
            if player not in winners:
                player.stats.update_game_result("loss")

    def reset_game(self):
        # Reset the game for a new round
        self.pot = 0
        self.community_cards = []
        self.deck = shuffle_deck(create_deck())
        self.current_round = "pre-flop"
        self.current_highest_bet = 0
        for player in self.players:
            player.reset_for_new_round()

def main():
    # Initialize players
    while True:
        try:
            num_players = int(input("Enter the number of players (2-10): "))
            if 2 <= num_players <= 10:
                break
            else:
                print("Please choose between 2 to 10 players.")
        except ValueError:
            print("Please enter a valid number between 2 to 10.")

    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        chip_count = 1000  # Starting chips
        position = i
        stats = PlayerStats()
        players.append(Player(name, chip_count, position, stats))

    game = Game(players)
    game.start_game()

if __name__ == "__main__":
    main()
