import holdem_helpers

# Generates deck and runs it
def run(hero, villain, board):
    deck = holdem_helpers.generate_deck(hero, villain, board)
    return run_sims(hero, villain, board, deck)


def run_sims(hero, villain, board_given, deck):
    # 2 players because it's heads up
    num_of_players = 2
    winner_list = [0] * num_of_players
    winner_list.append(0)  # Need an index for each player and the number of ties
    board_length = len(board_given)
    # If given a board, determine all combos
    if board_given:
        boards = holdem_helpers.generate_all_boards(deck, board_length)
    else:
        # Generates 100,000 boards 
        boards = holdem_helpers.generate_boards(deck, board_length)
    holdem_helpers.find_winner(hero, villain, board_given, boards, winner_list)
    holdem_helpers.print_results(hero, villain, winner_list)
    return holdem_helpers.odds(hero, villain, winner_list)
