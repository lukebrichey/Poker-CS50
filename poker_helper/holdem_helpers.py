# Adapted from  https://github.com/ktseng/holdem_calc/blob/master/holdem_functions.py

# Initializing card ranks + values and suits

suits = ("s", "c", "d", "h")
suit_index_dict = {"s": 0, "c": 1, "h": 2, "d": 3}
ranks_string = "AKQJT98765432"
ranks_dict = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for num in range(2, 10):
    ranks_dict[str(num)] = num
# No separate distinction for Royal Flush because Royal Flush is highest Straight Flush
hands_ranking = {"Straight Flush": 9, "Quads": 8, "Full House": 7,
                 "Flush": 6, "Straight": 5, "Three of a kind": 4,
                 "Two pair": 3, "Pair": 2, "High Card": 1}

# Generate deck, removing hole cards and board
def generate_deck(hero, villain, board):
    deck = []
    for suit in suits:
        for rank in ranks_string:
            deck.append(rank + suit)
    for i in range(len(hero)):
        deck.remove(hero[i])
        deck.remove(villain[i])
    for i in range(len(board)):
        deck.remove(board[i])

    return tuple(deck)

# Using Monte Carlo simulation a statistical method of Poker Calculators
# More info on https://en.wikipedia.org/wiki/Poker_calculator
# Essentially, run a lot of simulations and tally the number of wins for each player

# Generates 100,000 random boards, returns generator
def generate_boards(deck, board_length):
    import random
    for i in range(100000):
        yield random.sample(deck, 5 - board_length) 

# Generates every possible board for an exact calculation
# Only used when user gives a board, further explanation in DESIGN.md
def generate_all_boards(deck, board_length):
    import itertools
    return itertools.combinations(deck, 5 - board_length)

# Creates 7 card "board" by adding hand to 5 card board
def create_fulltable(hand, board):
    full_table = board.copy()
    full_table.extend(hand)
    return full_table

# Returns two lists, one with suits and their frequencies and ranks and their frequencies
def preprocess_board(table):
    # Creates list of suits and ranks
    board_suits, board_ranks = [0] * 4, [0] * 13
    # Creating a list with Ace at index 0
    for card in table:
        board_ranks[14 - ranks_dict[card[0]]] += 1
        board_suits[suit_index_dict[card[1]]] += 1
    return board_suits, board_ranks, max(board_suits)

# Returns the board with the highest number of suited cards, returns list
def generate_suit_board(full_table, flush_index):
    suit_board = []
    for card in full_table:
        if suit_index_dict[card[1]] == flush_index:  # card[1] is the suit of the card
            suit_board.append(card)
    return suit_board

# Checks for straight flush, returns list
def straight_flush_check(board_ranks):
    # Check for sequential order of cards
    contiguous_length, fail_index = 1, len(board_ranks) - 5
    for i in range(len(board_ranks)):
        current_val, next_val = board_ranks[i], board_ranks[i + 1]
        if current_val >= 1 and next_val >= 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, 14 - (i - 3)
        # Fail fast if straight not possible
        # This checks for wheel straight (Ace to 5)
        else:
            if i >= fail_index:
                if not board_ranks[0] >= 1 or 0 in board_ranks[9:12]:
                    break
                else:
                    return True, 5
            contiguous_length = 1
    return False, 0

# This is taken/adapted from the Github link above in the
# holdem_functions.py file and the detect_straight function
# On line 119, taken because it optimizes the search
def straight_check(board_ranks):
    # Check for sequential order of cards
    contiguous_length, fail_index = 1, len(board_ranks) - 5
    for i in range(len(board_ranks)):
        current_val, next_val = board_ranks[i], board_ranks[i+1]
        if current_val >= 1 and next_val >= 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, 14 - (i - 3)
        # Fail fast if straight not possible
        # This checks for wheel straight (Ace to 5)
        if i >= fail_index:
            if not board_ranks[0] >= 1 or 0 in board_ranks[9:12]:
                break
            else:
                return True, 5
        else:
            contiguous_length = 1
    return False, 0


# Checking for kickers
def detect_highest_quad_kicker(board_ranks):
    for i in range(len(board_ranks)):
        if board_ranks[i] < 4:
            return 14 - i

# Returns list of the two highest kickers that result from the three of a kind
def detect_three_of_a_kind_kickers(board_ranks):
    kickers = []
    for i in range(len(board_ranks)):
        if board_ranks[i] == 1:
            kickers.append(14 - i)
        if len(kickers) == 2:
            return kickers

# Returns the highest kicker available
def detect_highest_kicker(board_ranks):
    for i in range(len(board_ranks)):
        if board_ranks[i] == 1:
            return 14 - i

# Returns list: [kicker1, kicker2, kicker3]
def detect_pair_kickers(board_ranks):
    kickers = []
    for i in range(len(board_ranks)):
        if board_ranks[i] == 1:
            kickers.append(14 - i)
        if len(kickers) == 3:
            return kickers

# Returns a list of the five highest cards in the given board
def get_high_cards(board_ranks):
    high_cards = []
    for i in range(len(board_ranks)):
        if board_ranks[i] > 0:
            high_cards.append(14 - i)
    return high_cards

# Detects the best hand, returning the value of the hand 
# Hand values listed starting on line 9
def find_hand(hand, board, board_ranks, board_suits, max_suit):
    # Starting from strongest hands to weakest hands so we select best hand

    # Adding hand to the board 
    full_table = create_fulltable(hand, board)
    # Checking for flush/straight flush
    # If flush is true, then quads and full house are not possible
    if max_suit >= 5:
        flush_index = board_suits.index(max_suit)
        suit_board = generate_suit_board(full_table, flush_index)
        suit_board_ranks = preprocess_board(suit_board)[1]
        result, high_card = straight_flush_check(suit_board_ranks)
        if result:
            return [9, high_card]
        return [6, get_high_cards(board_ranks)]

    # Find which card value shows up the most and second most times
    current_max, max_val, second_max, second_max_val = 0, 0, 0, 0
    for i in range(len(board_ranks)):
        val = 14 - i  # board_ranks starts with Ace at index 0
        frequency = board_ranks[14 - val]  # Frequency of card
        if frequency > current_max:
            second_max, second_max_val = current_max, max_val
            current_max, max_val = frequency, val
        elif frequency > second_max:
            second_max, second_max_val = frequency, val

    # Check to see if there is a four of a kind
    if current_max == 4:
        return [8, max_val, detect_highest_quad_kicker(board_ranks)]
    # Check to see if there is a full house
    if current_max == 3 and second_max >= 2:
        return [7, max_val, second_max_val]
    # Check to see if there is a straight
    if len(full_table) >= 5:
        result, high_card = straight_check(board_ranks)
        if result:
            return [5, high_card]
    # Check to see if there is a three of a kind
    if current_max == 3:
        return [4, max_val, detect_three_of_a_kind_kickers(board_ranks)]
    # Check for pair
    if current_max == 2:
        # Check to see if there is a two pair
        if second_max == 2:
            return [3, max_val, second_max_val, detect_highest_kicker(board_ranks)]
        # Return pair
        else:
            return [2, max_val, detect_pair_kickers(board_ranks)]
    # Check for high cards
    return [1, get_high_cards(board_ranks)]

# Taken from Github project
def compare_hands(result_list):
    best_hand = max(result_list)
    winning_player_index = result_list.index(best_hand)
    # Check for tie
    if result_list[0] == result_list[1]:
        return 2  # Index for ties
    return winning_player_index
 
# Adapted from Github project
def find_winner(hero, villain, board_given, boards, winner_list):
    hands = [hero, villain]
    # Run simulations
    result_list = [None] * 2
    for remaining_board in boards:
        # Generate a new board
        if board_given:
            board = board_given.copy()
            board.extend(remaining_board)
        else:
            board = remaining_board
        # Find the best possible poker hand given the created board and the
        # hole cards and tally results
        for i in range(len(hands)):
            full_table = create_fulltable(hands[i], board)
            board_suits, board_ranks, max_suit = preprocess_board(full_table)
            result_list[i] = find_hand(hands[i], board, board_ranks, board_suits, max_suit)
        # Find the winner of the hand and tabulate results
        winner_index = compare_hands(result_list)
        winner_list[winner_index] += 1

def percentages(winner_list):
    percentages = []
    for wins in winner_list:
        winning_percentage = float(wins)/float(sum(winner_list))
        percentages.append(winning_percentage)
    return percentages

def odds(hero, villain, winner_list):
    odds = []
    ties = round(float(winner_list[2])/float(sum(winner_list)) * 100, 2)
    for i in range(2):
        winning_percentage = round(float(winner_list[i])/float(sum(winner_list)) * 100, 2)
        losing_percentage = round(100 - winning_percentage - ties, 2)
        odds.append(winning_percentage)
        odds.append(losing_percentage)
        odds.append(ties)
    print(odds)

    return odds

    
def print_results(hero, villain, winner_list):
    hands = [hero, villain]
    print("Win: ")
    for i in range(len(hands)):
        winning_percentage = round(float(winner_list[i])/float(sum(winner_list)) * 100, 2)
        print(str(hands[i]) + ": " + str(winning_percentage) + "%")
    ties = round(float(winner_list[2])/float(sum(winner_list)) * 100, 2)
    print("Ties: " + str(ties) + "%")
    
    