# poker_game.py

import random
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns

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
    pass

class InvalidActionError(Exception):
    pass

# Helper functions for cards
def create_deck():
    ranks = "23456789TJQKA"
    suits = "HDCS"
    return [(rank, suit) for rank in ranks for suit in suits]

def shuffle_deck(deck):
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

# PlayerStats class using Pandas DataFrame
class PlayerStats:
    def __init__(self, player_name):
        self.stats_df = pd.DataFrame(columns=[
            'Player',
            'Hands Played',
            'Wins',
            'Losses',
            'Folds',
            'Total Bets',
            'Aggressive Actions',
            'Total Pot Contribution'
        ])
        self.player_name = player_name
        self.stats_df.loc[0] = [
            player_name,
            0,  # Hands Played
            0,  # Wins
            0,  # Losses
            0,  # Folds
            0,  # Total Bets
            0,  # Aggressive Actions
            0   # Total Pot Contribution
        ]

    def update_game_result(self, result):
        self.stats_df.at[0, 'Hands Played'] += 1
        if result == "win":
            self.stats_df.at[0, 'Wins'] += 1
        elif result == "loss":
            self.stats_df.at[0, 'Losses'] += 1

    def update_aggressive_action(self):
        self.stats_df.at[0, 'Aggressive Actions'] += 1

    def update_fold(self):
        self.stats_df.at[0, 'Folds'] += 1

    def update_total_bet(self, amount):
        self.stats_df.at[0, 'Total Bets'] += amount

    def update_pot_contribution(self, amount):
        self.stats_df.at[0, 'Total Pot Contribution'] += amount

    def get_stats(self):
        return self.stats_df.copy()

    def display_stats(self):
        print(f"\nStatistics for {self.player_name}:")
        print(self.stats_df)

# Player class with is_human attribute and reference to Game instance
class Player:
    def __init__(self, name, chip_count, position, game, is_human=True):
        self.name = name
        self.chip_count = chip_count
        self.hand = []
        self.position = position
        self.current_bet = 0
        self.total_pot_contribution = 0
        self.is_folded = False
        self.is_all_in = False
        self.stats = PlayerStats(self.name)
        self.is_human = is_human
        self.decision_maker = DecisionMaker(self)
        self.game = game  # Reference to the Game instance

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
        self.stats.update_total_bet(amount)
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
        self.stats.update_total_bet(bet_amount)
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
        self.stats.update_total_bet(bet_increment)
        self.stats.update_pot_contribution(bet_increment)  # Pot contribution

    def receive_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return self.hand

    def display_status(self):
        return f"{self.name} - Chips: {self.chip_count}, Bet: {self.current_bet}, Hand: {'Folded' if self.is_folded else (pretty_print_hand(self.hand) if self.is_human else '[Hidden]')}"

    def reset_for_new_round(self):
        """Reset the player's state for a new round."""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.total_pot_contribution = 0

    def log_action(self, action, amount=None, game_state=None, pot_size=None, round_number=None):
        action_detail = f"{action}{' ' + str(amount) if amount is not None else ''}"
        logging.info(f"Player {self.position} ({self.name}): {action_detail}")
        # Log to Game's game_log DataFrame
        if self.game:
            new_row = pd.DataFrame({
                'Round': [round_number],
                'Player': [self.name],
                'Action': [action],
                'Amount': [amount],
                'Pot Size': [pot_size],
                'Game State': [game_state]
            })
            self.game.game_log = pd.concat([self.game.game_log, new_row], ignore_index=True)

# DecisionMaker class with AI logic using NumPy
class DecisionMaker:
    def __init__(self, player):
        self.player = player

    def get_action(self, game_state):
        if self.player.is_human:
            return self.get_human_action()
        else:
            return self.get_ai_action(game_state)

    def get_human_action(self):
        print(f"\n{self.player.name}'s turn. Available actions: 'fold', 'check', 'call', 'bet', 'raise'")
        while True:
            action = input("Enter your action: ").lower()
            if action in ['fold', 'check', 'call', 'bet', 'raise']:
                return action
            else:
                print("Invalid action. Please choose from 'fold', 'check', 'call', 'bet', 'raise'.")

    def get_ai_action(self, game_state):
        # Use NumPy to generate probabilities
        hand_strength = self.evaluate_hand_strength(game_state)
        risk_tolerance = np.random.uniform(0.1, 0.5)

        # Decide action based on hand strength and risk tolerance
        if hand_strength > risk_tolerance:
            if game_state.current_highest_bet == 0:
                action = 'bet'
            else:
                action = 'raise'
        elif hand_strength > risk_tolerance / 2:
            if game_state.current_highest_bet > self.player.current_bet:
                action = 'call'
            else:
                action = 'check'
        else:
            if game_state.current_highest_bet > self.player.current_bet:
                action = 'fold'
            else:
                action = 'check'

        print(f"{self.player.name} chooses to {action}")
        return action

    def evaluate_hand_strength(self, game_state):
        # Simplified hand strength evaluation using NumPy
        # In practice, you'd use more complex simulations or algorithms
        # For demonstration, assign a random strength
        return np.random.uniform(0, 1)

    def get_bet_amount(self, min_bet=0):
        if self.player.is_human:
            while True:
                try:
                    amount = int(input(f"Enter bet amount (minimum {min_bet}): "))
                    if amount >= min_bet and amount <= self.player.chip_count:
                        return amount
                    else:
                        print(f"Invalid amount. Please bet an amount between {min_bet} and your chip count ({self.player.chip_count}).")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            # AI bet amount logic
            amount = min(self.player.chip_count, max(min_bet, int(self.player.chip_count * np.random.uniform(0.1, 0.5))))
            print(f"{self.player.name} bets {amount}")
            return amount

    def get_raise_amount(self, min_raise):
        if self.player.is_human:
            while True:
                try:
                    amount = int(input(f"Enter raise amount (minimum {min_raise}): "))
                    if amount >= min_raise and amount <= self.player.chip_count:
                        return amount
                    else:
                        print(f"Invalid amount. Please ensure you have enough chips to raise at least {min_raise} and up to your chip count ({self.player.chip_count}).")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            # AI raise amount logic
            amount = min(self.player.chip_count, max(min_raise, int(self.player.chip_count * np.random.uniform(0.1, 0.5))))
            print(f"{self.player.name} raises by {amount}")
            return amount

# Game class with automated data visualization and post-game analysis
class Game:
    def __init__(self, players_info):
        self.players = []
        for player_info in players_info:
            player = Player(
                name=player_info['name'],
                chip_count=player_info['chip_count'],
                position=player_info['position'],
                game=self,
                is_human=player_info['is_human']
            )
            self.players.append(player)
        self.small_blind = 10  # Set as per game rules
        self.big_blind = 20    # Set as per game rules
        self.dealer_position = 0
        self.current_round = "pre-flop"
        self.community_cards = []
        self.pot = 0
        self.deck = []
        self.current_highest_bet = 0
        self.game_log = pd.DataFrame(columns=['Round', 'Player', 'Action', 'Amount', 'Pot Size', 'Game State'])
        self.round_number = 0
        self.all_player_stats = pd.DataFrame()  # To collect stats across rounds

    def start_game(self):
        while True:
            self.round_number += 1
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
        # At the end of the game, display stats and generate visualizations
        self.end_game_session()

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
        self.end_round()

    def deal_cards(self):
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.pop())
        print("\nPlayers' Hands:")
        for player in self.players:
            print(f"{player.name}'s hand: {pretty_print_hand(player.hand) if player.is_human else '[Hidden]'}")

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
                    player.log_action(
                        action, amount=0, game_state=self.current_round, pot_size=self.pot, round_number=self.round_number
                    )
                    # If only one player remains, they win the pot
                    if len(players_in_round) == 1:
                        self.end_round()
                        return
                elif action == 'check':
                    if player.current_bet < self.current_highest_bet:
                        print("You cannot check when there is a bet. You must call or raise.")
                        betting_complete = False
                        continue
                    player.log_action(
                        action, amount=0, game_state=self.current_round, pot_size=self.pot, round_number=self.round_number
                    )
                elif action == 'call':
                    call_amount = self.current_highest_bet - player.current_bet
                    player.call(self.current_highest_bet)
                    self.pot += call_amount
                    if player.is_all_in:
                        print(f"{player.name} is all-in!")
                    player.log_action(
                        action, amount=call_amount, game_state=self.current_round, pot_size=self.pot, round_number=self.round_number
                    )
                elif action == 'bet':
                    min_bet = max(self.big_blind, self.current_highest_bet)
                    bet_amount = player.decision_maker.get_bet_amount(min_bet)
                    self.current_highest_bet = bet_amount
                    player.bet(bet_amount)
                    self.pot += bet_amount
                    betting_complete = False
                    player.log_action(
                        action, amount=bet_amount, game_state=self.current_round, pot_size=self.pot, round_number=self.round_number
                    )
                elif action == 'raise':
                    min_raise = self.big_blind
                    raise_amount = player.decision_maker.get_raise_amount(min_raise)
                    player.raise_bet(raise_amount, self.current_highest_bet)
                    self.pot += (player.current_bet - self.current_highest_bet)
                    self.current_highest_bet = player.current_bet
                    betting_complete = False
                    player.log_action(
                        action, amount=raise_amount, game_state=self.current_round, pot_size=self.pot, round_number=self.round_number
                    )
                else:
                    print("Invalid action.")
                # Check if all active players have matched the highest bet
                active_players = [player for player in self.players if not player.is_folded and not player.is_all_in]
                if any(player.current_bet < self.current_highest_bet for player in active_players):
                    betting_complete = False
                else:
                    betting_complete = True

    def end_round(self):
        # Hand Evaluation
        active_players = [player for player in self.players if not player.is_folded]
        if not active_players:
            print("All players have folded. No winner.")
            return

        best_hands = {}
        for player in active_players:
            best_hands[player] = best_hand(player.hand, self.community_cards)
            print(f"{player.name}'s best hand: {hand_name(best_hands[player][0])}")
            print(f"{player.name}'s hand: {pretty_print_hand(player.hand)}")

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

        # Collect player stats at the end of the round
        for player in self.players:
            self.all_player_stats = pd.concat([self.all_player_stats, player.stats.get_stats()], ignore_index=True)

        # Display player stats
        for player in self.players:
            player.stats.display_stats()

    def reset_game(self):
        # Reset the game for a new round
        self.pot = 0
        self.community_cards = []
        self.deck = shuffle_deck(create_deck())
        self.current_round = "pre-flop"
        self.current_highest_bet = 0
        for player in self.players:
            player.reset_for_new_round()

    def end_game_session(self):
        # Save game log and player stats to CSV
        self.game_log.to_csv('game_log.csv', index=False)
        self.all_player_stats.to_csv('player_stats.csv', index=False)

        # Generate data visualizations and analysis
        self.generate_data_visualizations()

    def generate_data_visualizations(self):
        print("\nGenerating data visualizations and analysis...")

        # Load game log and player stats
        game_log = self.game_log
        all_stats = self.all_player_stats

        # Trend Analysis
        # Group data by 'Hands Played' and 'Player' to see trends over rounds
        trend_data = all_stats.groupby(['Player', 'Hands Played']).sum().reset_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=trend_data, x='Hands Played', y='Wins', hue='Player', marker='o')
        plt.title('Wins Over Hands Played')
        plt.xlabel('Hands Played')
        plt.ylabel('Wins')
        plt.legend(title='Player')
        plt.savefig('trend_analysis.png')
        plt.show()

        # Leaderboard
        leaderboard = all_stats.groupby('Player').sum().reset_index()
        leaderboard['Win Rate'] = leaderboard['Wins'] / leaderboard['Hands Played']
        leaderboard = leaderboard.sort_values(by='Wins', ascending=False)
        print("\nLeaderboard:")
        print(leaderboard[['Player', 'Wins', 'Losses', 'Win Rate']])

        # Plotting leaderboard
        plt.figure(figsize=(10, 6))
        sns.barplot(data=leaderboard, x='Player', y='Wins')
        plt.title('Leaderboard - Total Wins')
        plt.xlabel('Player')
        plt.ylabel('Total Wins')
        plt.savefig('leaderboard.png')
        plt.show()

        # Clustering players based on behavior
        behavior_metrics = leaderboard[['Aggressive Actions', 'Folds', 'Total Bets', 'Total Pot Contribution']]
        scaler = StandardScaler()
        scaled_metrics = scaler.fit_transform(behavior_metrics)
        if len(leaderboard) >= 2:
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(scaled_metrics)
            leaderboard['Cluster'] = kmeans.labels_
            print("\nPlayer Clusters based on behavior:")
            print(leaderboard[['Player', 'Cluster']])

            # Visualize clusters
            plt.figure(figsize=(8, 6))
            sns.scatterplot(
                x=leaderboard['Aggressive Actions'],
                y=leaderboard['Total Bets'],
                hue=leaderboard['Cluster'],
                palette='viridis',
                s=100
            )
            for i, player in enumerate(leaderboard['Player']):
                plt.text(
                    leaderboard['Aggressive Actions'].iloc[i]+0.1,
                    leaderboard['Total Bets'].iloc[i]+0.1,
                    player
                )
            plt.title('Player Clusters Based on Behavior')
            plt.xlabel('Aggressive Actions')
            plt.ylabel('Total Bets')
            plt.legend(title='Cluster')
            plt.savefig('player_clusters.png')
            plt.show()
        else:
            print("Not enough players to perform clustering.")

def main():
    # Initialize players
    while True:
        try:
            num_players = int(input("Enter the total number of players (2-10): "))
            if 2 <= num_players <= 10:
                break
            else:
                print("Please choose between 2 to 10 players.")
        except ValueError:
            print("Please enter a valid number between 2 to 10.")

    players_info = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        chip_count = 1000  # Starting chips
        position = i
        while True:
            is_human_input = input(f"Is {name} a human player? (yes/no): ").lower()
            if is_human_input in ['yes', 'y']:
                is_human = True
                break
            elif is_human_input in ['no', 'n']:
                is_human = False
                break
            else:
                print("Please answer 'yes' or 'no'.")
        players_info.append({
            'name': name,
            'chip_count': chip_count,
            'position': position,
            'is_human': is_human
        })

    game = Game(players_info)
    game.start_game()

if __name__ == "__main__":
    main()
