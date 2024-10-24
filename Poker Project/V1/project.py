from card_utils import create_deck, shuffle_deck, deal_cards, pretty_print_hand
from poker_logic import best_hand, compare_hands, hand_name

def main():
    print("Welcome to Texas Hold'em Simulator")

    while True:
        while True: # Keep asking until valid input is provided
            try:
                num_players = int(input("Enter the number of players (2-10): "))
                if 2 <= num_players <= 10:
                    break
                else:
                    print("Please choose between 2 to 10 players.")
            except ValueError: # Catch non-integer inputs
                print("Please enter a valid number between 2 to 10.")

        simulate_round(num_players)

        play_again = input("Play another round? (yes/no): ").lower()
        while play_again not in ["yes", "no", "y", "n"]:
            play_again = input("Please answer with 'yes' or 'no'. Play another round?")

        if play_again in ["no", "n"]:
            print("Thanks for playing!")
            break


def simulate_round(num_players=2):
    deck = shuffle_deck(create_deck())

    # Step 1 & 2: Setup and Deal
    player_hands, community_cards = deal_cards(deck, num_players)

    # For simplicity, skipping the betting rounds
    # However, for complete game simulation, they would be integrated here

    # Show initial cards
    for i, hand in enumerate(player_hands, start=1):
        print(f"Player {i}'s hand: {pretty_print_hand(hand)}")

    print("Community Cards:", pretty_print_hand(community_cards[:3])) # Flop
    # ... Simulate betting ...
    print("Community Cards:", pretty_print_hand(community_cards[:4])) # Turn
    # ... Simulate betting ...
    print("Community Cards:", pretty_print_hand(community_cards))     # River
    # ... Simulate betting ...

    # Step 4 & 5: Hand Evaluation & Determine Winner
    best_hands = [best_hand(hand, community_cards) for hand in player_hands]

    # Logic for determining the best hand and winners
    winning_hand_value = max(best_hands, key=lambda x: (x[0], x[1], x[2]))
    winners = [i for i, hand in enumerate(best_hands, start=1) if hand == winning_hand_value]

    # Print the outcome
    if len(winners) == 1:
        print(f"Player {winners[0]} wins with a {hand_name(winning_hand_value[0])}!")
    else:
        print(f"It's a tie between players {', '.join(map(str, winners[:-1]))} and {winners[-1]} with a {hand_name(winning_hand_value[0])}!")

if __name__ == "__main__":
    main()