# Poker CS50

Our project is a web application primarily constructed through Python, Flask, HTML, JavaScript, and CSS. In order to run the project, the user must enter the folder's directory with 'cd poker_helper' and execute 'flask run'. This will create a link to access the website, where the user can test the functionality of the program.

The purpose of the program is to calculate the Win, Loss, and Tie percentages of either player in a heads-up Texas Hold 'Em poker game, at any spot or street. The user can drag-and-drop cards from the card bank at the top of the page into P1 and P2's placeholder hole cards and onto the placeholder board. The user will not be allowed to re-use the same card after dropping it into a placeholder location. As long as both players have two hole cards, the user can click the "Calculate Odds" button, and the program will return Win, Loss, and Tie odds at any stage of the hand (pre-flop, flop, turn, river). After the user calculates odds, the odds will display and the hand will reset, and the user can drag-and-drop a new hand. 

The program calculates each player's odds by running Python simulations of the hand, and accurately matches existing poker calculators. For functionality testing purposes, it can be useful to run a hand's odds using our calculator and comparing it to the odds of an online calculator such as: https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem.

Video URL: https://www.youtube.com/watch?v=AeZUOVT-j7o
