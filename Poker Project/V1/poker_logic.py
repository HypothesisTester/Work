from itertools import combinations

# Card value mappings
RANK_VALUES = {rank: index for index, rank in enumerate("23456789TJQKA", start=2)}

# Hand ranks
HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND, STRAIGHT_FLUSH, ROYAL_FLUSH = range(10)

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
        ROYAL_FLUSH: "Royal Flush"
    }
    return rank_names.get(rank, "Unknown Hand")


def hand_value(hand):
    rank_counts = {rank: 0 for rank, _ in RANK_VALUES.items()}
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
            return(ROYAL_FLUSH, ['A'], [])
        elif values == [2, 3, 4, 5, 14]:
            return (STRAIGHT_FLUSH, ['5'], [])
        else:
            high_card = sorted(hand, key=lambda card: RANK_VALUES[card[0]])[-1][0]
            return (STRAIGHT_FLUSH, [high_card], [])

    if is_flush(hand):
        ranks = sorted((card[0] for card in hand), key=lambda x: RANK_VALUES[x], reverse=True)
        return(FLUSH, ranks, [])

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
        one_pair_kicker = sorted([rank for rank, count in rank_counts if count == 1], key=lambda x: RANK_VALUES[x], reverse=True)
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
    best_rank = (-1, [])
    # Compare hands based on the primary and secondary evaluation metrics
    for combo in combinations(all_cards, 5):

        current_value = hand_value(sorted(combo, key=lambda card: RANK_VALUES[card[0]]))

        if current_value > best_rank:
            best_rank = current_value

    return best_rank


def compare_hands(hand1, hand2):
    # Compares two poker hands and returns the winning hand. If it's a tie, returns None

    value1 = hand_value(hand1)
    value2 = hand_value(hand2)

    if value1[0] > value2[0]:  # Compare hand ranks first
        return 1
    elif value1[0] < value2[0]:
        return -1
    else:  # If hand ranks are the same, compare primary values, then kickers
        for v1, v2 in zip(value1[1], value2[1]):
            if RANK_VALUES[v1] > RANK_VALUES[v2]:
                return 1
            elif RANK_VALUES[v1] < RANK_VALUES[v2]:
                return -1
        for k1, k2 in zip(value1[2], value2[2]):
            if RANK_VALUES[k1] > RANK_VALUES[k2]:
                return 1
            elif RANK_VALUES[k1] < RANK_VALUES[k2]:
                return -1
    return 0  # If the function hasn't returned by now, it's a tie
