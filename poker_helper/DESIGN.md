Overview:

This project was meant to recreate the poker calculators seen online like this one: https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem. The way these types of calculators usually work is by running a large amount of simulations, randomizing the flop, turn, and river and determines the winner of each simulation. These are then accumulated and winning percentages are calculated. This gets the probability to around the nearest percent. This method is called Monte Carlo simulations, and is utilized in our implementation when the user does not give any board cards. For exact calculations, programs will compute every possible combination of flop, turn, and river. For heads up, this gives about 1.7 million combinations (nCr(48, 5)). This amount of simulations can begin to bog down runtime, and is only used when the user has given a flop. As such, we simulate 100,000 times when we are not given a flop. We use exact calculations when given a flop because the total number of combinations for two cards (990 combinations) is much lower than the 100,000 simulations we normally run. This amount gets our calculation to almost exactly the same as the calculator linked above.

Design:

    The first step in running a calculator like this is determining the format of cards. This is easy,
as it is pretty much standard in poker to format cards with their rank and suit in lowercase like this:
"Ad" for Ace of diamonds. However, to keep each card to a 2 character format we format 10s to Ts. 
This just keeps the consistency throughout the format. We also assign numerical values to each rank, 
1 - 14, just so we can further differentiate through cards. Finally, we have a dictionary containing 
the suit indexes. This is just for consistencies for the lists we use later in our project. We also 
denote the rankings to each type of hand (Straight Flush, Four of a Kind, Full House, Flush, Straight, 
Three of a Kind, Two Pair, Pair, and Pair) with the numbers 1 - 9, with one being a high card. We did 
not make a separate distinction between straight flush and royal flush since a royal flush is just the 
highest straight flush. Finally, there is a "ranks_string" that just has all the different cards so it 
makes it easier to generate the deck. These constants are all at the top of holdem_helpers.py.
    After we define our constants, we begin to define our helper functions. All of these functions are 
contained in holdem_helpers.py. First, before we begin to run our simulations we must generate the 52 card 
deck. This is done by concatenating each rank to each different suit using nested for-loops. We then 
remove each card in both the hero's hand and villain's hand, as well as any cards on the board using 
more for-loops and deck.remove(). We return the deck as a tuple just so we do not have to worry about 
accidentally modifying it in our code. The function run(), contained in holdem_calc.py, calls the 
generate_deck() function. After the deck is generated, we are now able to call run_simulations() 
within our function run(). 
    run_simulation takes the parameters of hero, villain, board, and the deck. The hero and villain
hands are lists formatted like ["Ad", "Qs"] with the board being the same format. run_simulations() 
initializes winner_list, a list with a length of 3, with the first element being the number of wins 
for the hero, the second element being the number of wins for the villain, and the final element being 
the number of ties. It also declares a variable called board_length, which just lets the program know 
the length of the board the user has given. Then, our program begins to generate boards. As briefly 
stated in the overview, we run Monte Carlo simulations when the user does not give any board cards. 
This is to avoid bogging down our runtime. Conversely, when we are given a flop or flop + turn or 
flop + turn + river we generate all the combinations for the reasons stated in the overview. The 
first is done with the function generate_boards(), defined in holdem_helpers.py,  which randomly 
chooses cards for the board. It does this using the random module and "yielding" a sample of 
100,000 random boards. We used yield because this produces a generator that takes up less memory 
and decreases runtime. When given a board, we call generate_all_boards() and using the itertools 
module we generate all possible combinations with itertools.combinations(), which also returns a 
generator. Once this is done, we can being to actually calculate the winners of each board using 
find_winners().
    find_winners() is the "main" function of our program. It is defined in holdem_helpers.py. Basically 
the function finds each player's hand and compares it to one another, determining which player won, 
lost, or if they tied. First, it creates a "full table", adding the hole cards to the board to create 
the 7 card selection from which a hand is found. This is done through the create_full_table() function. 
Next, we get some information about the board through preprocess_board() which returns the ranks and 
their respective frequencies, the same thing for the suits, and then the frequency of the most common 
suit. These are then used in the find_hand() function. The find_hand() function calls many different
functions. First, the function checks if max_suit (the frequency of the most common suit) is greater
than or equal to 5, which would signifiy some sort of flush. If there are 5 cards of the same suit, 
then four of a kind or full house are not possible so we either return straight flush or flush. 
To do this,it generates a "suit board", which is basically a board of all the cards with the same 
suit. It then runs preprocess() on this board and gets the suit_board_ranks which is the frequency 
of each card. Then we can run straight_flush_check which goes through each element in suit_board_ranks 
checking to see if there is a 5-long continuous string of cards (frequencies of at least 1 in a 5-long 
streak of elements). There is also a fail index at index 8 because once you have hit index 8 and not 
found a straight, then there is no straight possible. We also have an edge-case check for a wheel, 
Ace through 5. straight_flush_check returns 9 (the value of a straight flush) and the high card of 
the straight. If straight_flush_check returns false then the function returns 6 (value of flush) 
and all of its cards. Then, the function checks for quads by seeing if any of the frequencies in 
board_ranks are equal to 4, returning the value of a four of a kind as well as the high cards. 
Similarly, we check for full house by seeing if there is a frequency of 3 and 2 in board_ranks, 
returning 7 and the two cards it consists of. Then it checks for a straight using straight_check 
which functions virtually the same as straight_flush_check. Finally, we check for three of a kind, 
two pair, pair, by seeing if their is a frequency of 3, or 2 frequencies of 2, or one frequency 
of 2 in board_ranks. If none of these are true, we return 1 for a high card and find all the high cards. 
Each of these non-5 card hands have their own respective functions to find the kicker. 
After the hand of each player is determined, compare_hands() is called which simply calls max() 
on the two hands and returns the index of the winning player. It also checks if the hands are 
the same, in which case it returns 2, the tie index. The function does this over and over until 
it finally calculates the percentages with some simple arithmetic. 

