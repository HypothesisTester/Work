import logging
import time

# Custom Exception Classes
class InsufficientChipsError(Exception):
    """Raised when a player does not have enough chips for a bet or call."""
    pass

class InvalidActionError(Exception):
    """Raised when an invalid action is attempted."""
    pass

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Player:
    def __init__(self, chip_count, position, stats):
        self.chip_count = chip_count
        self.hand = []
        self.position = position
        self.current_bet = 0
        self.total_pot_contribution = 0
        self.is_folded = False
        self.is_all_in = False
        self.stats = stats

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
            raise ValueError("Insufficient chips for the bet.")
        self.chip_count -= amount
        self.current_bet = amount
        self.total_pot_contribution += amount
        self.stats.update_aggressive_action()  # Aggressive action
        self.stats.update_vpip_action()  # VPIP action
        self.stats.update_pot_contribution(amount)  # Pot contribution
        if self.chip_count == 0:
            self.is_all_in = True

    def check(self):
        pass

    def call(self, current_highest_bet):
        bet_amount = current_highest_bet - self.current_bet
        if bet_amount > self.chip_count:
            # Option: Player goes all-in if they don't have enough chips to call
            bet_amount = self.chip_count
            self.is_all_in = True
        self.chip_count -= bet_amount
        self.current_bet = current_highest_bet
        self.total_pot_contribution += bet_amount
        self.stats.update_pot_contribution(bet_amount)  # Pot contribution

    def raise_bet(self, raise_amount, current_highest_bet):
        total_bet = current_highest_bet + raise_amount
        if total_bet > self.chip_count:
            # Option: Player goes all-in if they don't have enough chips to raise
            raise_amount = self.chip_count - current_highest_bet
            total_bet = self.chip_count
            self.is_all_in = True
        self.chip_count -= total_bet - self.current_bet
        self.current_bet = total_bet
        self.total_pot_contribution += total_bet - self.current_bet
        self.stats.update_aggressive_action()  # Aggressive action
        self.stats.update_vpip_action()  # VPIP action
        self.stats.update_pot_contribution(total_bet - self.current_bet)  # Pot contribution

    def receive_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return self.hand

    def display_status(self):
        return f"Chips: {self.chip_count}, Bet: {self.current_bet}, Hand : {'Folded' if self.is_folded else self.hand}"

    def reset_for_new_round(self):
        """Reset the player's state for a new round."""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
        self.total_pot_contribution = 0

    def post_small_blind(self, amount):
        if self.chip_count < amount:
            raise InsufficientChipsError("Not enough chips for the big blind.")
        self.bet(amount)

    def post_big_blind(self, amount):
        if self.chip_count < amount:
            raise InsufficientChipsError("Not enough chips for the big blind.")
        self.bet(amount)

    def update_position(self, new_position):
        self.position = new_position

    def log_action(self, action, amount=None):
        action_detail = f"{action}{' ' + str(amount) if amount is not None else ''}"
        logging.info(f"Player {self.position}: {action_detail}")


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


class DecisionMaker:
    def __init__(self, player):
        self.player = player

    def make_decision(self, decision_function, timeout=10):
        """
        Simulates a player making a decision with a timeout.
        decision_function: The function to call for making a decision.
        timeout: Time in seconds before defaulting to a fold.
        """
        start_time = time.time()
        decision = None
        while time.time() - start_time < timeout and decision is None:
            decision = decision_function() # This should be a blocking call
        if decision is None:
            self.fold()
            return "Folded due to timeout"
        return decision


class Game:

    def __init__(self, players):
        # Initialization logic
        self.players = players
        self.small_blind = 10  # Set as per game rules
        self.big_blind = 20    # Set as per game rules
        self.dealer_position = 0
        self.current_round = "pre-flop"
        self.community_cards = []
        self.pot = 0

    def play_betting_round(self):
        # Conduct a betting round
        for player in self.get_active_players():
            if not player.is_folded:
                action = self.get_player_action(player)
                self.process_player_action(player, action)

    def process_player_action(self, player, action):
        # Process individual player actions
        if action == "fold":
            player.fold()
        elif action == "check":
            player.check()
        elif action == "call":
            player.call(self.get_current_highest_bet())
        elif action == "bet":
            amount = self.get_bet_amount(player)
            player.bet(amount)
        elif action == "raise":
            raise_amount = self.get_raise_amount(player)
            player.raise_bet(raise_amount, self.get_current_highest_bet())

        # Update the pot and log the action for all actions
        self.pot += player.current_bet
        player.log_action(action, player.current_bet)

    def get_player_action(self, player):
        # Get action from player
        print(f"{player.position}'s turn. Available actions: 'fold', 'check', 'call', 'bet', 'raise'")
        action = input("Enter your action: ")
        return action

    def get_bet_amount(self, player):
        # Determine bet amount
        while True:
            try:
                amount = int(input("Enter bet amount: "))
                if amount > 0 and amount <= player.chip_count:
                    return amount
                else:
                    print("Invalid amount. Please bet an amount within your chip count.")
            except ValueError:
                print("Please enter a valid number.")

    def get_raise_amount(self, player):
        # Determine raise amount
        while True:
            try:
                amount = int(input("Enter raise amount: "))
                if amount > 0 and (player.current_bet + amount) <= player.chip_count:
                    return amount
                else:
                    print("Invalid amount. Please ensure you have enough chips to raise.")
            except ValueError:
                print("Please enter a valid number.")

    def process_player_action(self, player, action):
        # Process individual player actions
        if action == "fold":
            player.fold()
        elif action == "check":
            player.check()
        elif action == "call":
            player.call(self.get_current_highest_bet())
        elif action == "bet":
            amount = self.get_bet_amount(player)
            player.bet(amount)
        elif action == "raise":
            raise_amount = self.get_raise_amount(player)
            player.raise_bet(raise_amount, self.get_current_highest_bet())

    def get_active_players(self):
        # Get list of players who haven't folded
        return [player for player in self.players if not player.is_folded]

    def get_current_highest_bet(self):
         # Determine the current highest bet
        return max(player.current_bet for player in self.players)

    def end_game(self):
        # End the game and determine the winner
        winner = self.determine_winner()
        winner.chip_count += self.pot
        self.reset_game()

    def determine_winner(self):
        # Hand Evaluation
        best_hands = [best_hand(player.hand, self.community_cards) for player in self.get_active_players()]

        # Logic for determining the best hand and winners
        winning_hand_value = max(best_hands, key=lambda x: (x[0], x[1], x[2]))
        winners = [player for player, hand in zip(self.get_active_players(), best_hands) if hand == winning_hand_value]

        # Determine if it's a tie
        is_tie = len(winners) > 1
        return winners, is_tie, winning_hand_value

    def reset_game(self):
        # Reset the game for a new round
        self.pot = 0
        for player in self.players:
            player.reset_for_new_round()

    def announce_winner(self):
        # Announce the game winner
        winners, is_tie, winning_hand_value = self.determine_winner()
        if not is_tie:
            print(f"Player {winners[0].position} wins with a {hand_name(winning_hand_value[0])}!")
        else:
            winner_positions = [player.position for player in winners]
            print(f"It's a tie between players {', '.join(map(str, winner_positions))} with a {hand_name(winning_hand_value[0])}!")

class PlayerManager:
    def __init__(self, players):
        self.players = players

    def get_active_players(self):
        # Get list of players who haven't folded
        return [player for player in self.players if not player.is_folded]

    def reset_for_new_round(self):
        # Reset each player's state for a new round
        for player in self.players:
            player.reset_for_new_round()

    # Add any other player-specific methods here, e.g., adding/removing players


class BettingSystem:
    def __init__(self):
        self.pot = 0

    def play_betting_round(self):
        # Conduct a betting round
        for player in self.get_active_players():
            if not player.is_folded:
                action = self.get_player_action(player)
                self.process_player_action(player, action)

    def process_player_action(self, player, action):
        # Process individual player actions
        if action == "fold":
            player.fold()
        elif action == "check":
            player.check()
        elif action == "call":
            player.call(self.get_current_highest_bet())
        elif action == "bet":
            amount = self.get_bet_amount(player)
            player.bet(amount)
        elif action == "raise":
            raise_amount = self.get_raise_amount(player)
            player.raise_bet(raise_amount, self.get_current_highest_bet())

        # Update the pot and log the action for all actions
        self.pot += player.current_bet
        player.log_action(action, player.current_bet)

    def get_player_action(self, player):
        # Get action from player
        print(f"{player.position}'s turn. Available actions: 'fold', 'check', 'call', 'bet', 'raise'")
        action = input("Enter your action: ")
        return action

    def get_bet_amount(self, player):
        # Determine bet amount
        while True:
            try:
                amount = int(input("Enter bet amount: "))
                if amount > 0 and amount <= player.chip_count:
                    return amount
                else:
                    print("Invalid amount. Please bet an amount within your chip count.")
            except ValueError:
                print("Please enter a valid number.")

    def get_raise_amount(self, player):
        # Determine raise amount
        while True:
            try:
                amount = int(input("Enter raise amount: "))
                if amount > 0 and (player.current_bet + amount) <= player.chip_count:
                    return amount
                else:
                    print("Invalid amount. Please ensure you have enough chips to raise.")
            except ValueError:
                print("Please enter a valid number.")

    def get_current_highest_bet(self, players):
        # Determine the current highest bet
        return max(player.current_bet for player in players)

    def update_pot(self, amount):
        # Update the pot with the given amount
        self.pot += amount


class GameState:
    def __init__(self):
        self.current_round = "pre-flop"
        self.community_cards = []
        self.dealer_position = 0

    def update_round(self, new_round):
        # Update the current round
        self.current_round = new_round

    def update_community_cards(self, cards):
        # Update community cards
        self.community_cards.extend(cards)

    def advance_dealer_position(self):
        # Advance the dealer position for the next round
        self.dealer_position = (self.dealer_position + 1) % num_players

    # Add any other game state specific methods here

class WinnerDetermination:
    def determine_winner(self):
        # Hand Evaluation
        best_hands = [best_hand(player.hand, self.community_cards) for player in self.get_active_players()]

        # Logic for determining the best hand and winners
        winning_hand_value = max(best_hands, key=lambda x: (x[0], x[1], x[2]))
        winners = [player for player, hand in zip(self.get_active_players(), best_hands) if hand == winning_hand_value]

        # Determine if it's a tie
        is_tie = len(winners) > 1
        return winners, is_tie, winning_hand_value

    def announce_winner(self):
        # Announce the game winner
        winners, is_tie, winning_hand_value = self.determine_winner()
        if not is_tie:
            print(f"Player {winners[0].position} wins with a {hand_name(winning_hand_value[0])}!")
        else:
            winner_positions = [player.position for player in winners]
            print(f"It's a tie between players {', '.join(map(str, winner_positions))} with a {hand_name(winning_hand_value[0])}!")


    def reset_game(self):
        # Reset the game for a new round
        self.pot = 0
        for player in self.players:
            player.reset_for_new_round()

    # Add any other winner determination specific methods here


class Game:
    def __init__(self, players):
        self.player_manager = PlayerManager(players)
        self.betting_system = BettingSystem()
        self.game_state = GameState()
        self.winner_determination = WinnerDetermination()

    def play_round(self):
        # Play a single round of the game
        self.betting_system.play_betting_round(self.player_manager.get_active_players())
        # ... other round-specific logic ...

    def end_game(self):
        # End the game and determine the winner
        winners, winning_hand = self.winner_determination.determine_winner(
            self.player_manager.get_active_players(), self.game_state.community_cards)
        self.winner_determination.announce_winner(winners, winning_hand)
        self.winner_determination.reset_game(self.player_manager.players, self.game_state, self.betting_system)

    # Add any other game control methods here

