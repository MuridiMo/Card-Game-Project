# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                   Computer Project #10
#           
#   Aces Up is a popular solitaire card game which is played 
#   by one person with a standard 52-card deck of cards. 
#   this program will allow the user to play a simplified version 
#   of Aces Up, with the program managing the game.
#
# # # # # # # # # # #  # # # # # # # # #  # # # # # # # # # # # # #
import cards  # required !!!
import random

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():

    """ Initalizes the game The function has no parameters and returns the
        starting state of the game with the three data structures"""

    deck = cards.Deck()
    deck.shuffle()
    tableau = [[], [], [], []]
    for i in range(4):
        card = deck.deal()
        tableau[i].append(card)
    foundation = []

    return (deck, tableau, foundation)
    
def deal_to_tableau( tableau, stock):

    '''deal cards to the tableau.This function has two parameters: the data structure representing the stock and the data structure representing the tableau. It will deal a card from the stock to each column of the tableau, unless the stock has fewer than 4 cards; in which case it will just deal a card to consecutive columns until the stock is empty. '''

    for i in range(min(4, len(stock))):
        for j in range (len(tableau)):
            if i == j:
                card = stock.deal()
                tableau[i].append(card)

def validate_move_to_foundation(tableau, from_col):

    ''' determine if a requested move to the foundation is valid. 
        The function should not modify the tableau in any case.'''

    if len(tableau[from_col]) == 0:
        print(f"Error, empty column: {from_col}")
        return False

    card = tableau[from_col][-1]
    suit = card.suit()
    rank = card.rank()
    if rank == 1:
        rank = 14

    # Check all columns, including those before from_col
    for col in range(len(tableau)):
        if len(tableau[col]) == 0 or col == from_col:
            continue

        other_card = tableau[col][-1]
        other_suit = other_card.suit()
        other_rank = other_card.rank()

        if other_rank == 1:
            other_rank = 14
        
        if other_rank == 14 and other_suit == suit:
            return True
        
        # if theres a card of the same suit and higher rank in a different column return true
        if suit == other_suit and rank < other_rank:
            return True
    print("\nError, cannot move {}.".format(card))
    return False
    
def move_to_foundation( tableau, foundation, from_col ):

    '''move a card from the tableau to the foundation.This function has three parameters: the data structure representing the tableau, the data structure representing the foundation, and an int indicating the index of the column whose bottom card should be moved. '''

    if validate_move_to_foundation(tableau, from_col):
        card = tableau[from_col].pop()
        return foundation.append(card)


def validate_move_within_tableau( tableau, from_col, to_col ):

    '''determine if a requested move to the foundation is valid. The
    function should not modify the tableau in any case. This function has two parameters: the data structure representing the tableau and an int indicating the
    index of the column whose bottom card should be moved.  '''

    # if the to column isnt empty print an error message
    if len(tableau[to_col])>= 1:
        print("\nError, target column is not empty: {}".format(to_col+1))
        return False
    
    # if the from column is empty print an error message
    if tableau[from_col] == []:
        print("\nError, no card in column: {}".format(from_col+1))
        return False
    
    return True



def move_within_tableau( tableau, from_col, to_col ):

    '''move a card from the tableau to the foundation.
    This function has three parameters: the data structure representing the 
    tableau, an int indicating the column whose bottom card should be moved, 
    and an int indicating the column the card should be moved to '''

    if validate_move_within_tableau(tableau, from_col, to_col):
        card = tableau[from_col].pop()
        return tableau[to_col].append(card)
    


        
def check_for_win( tableau, stock ):

    '''check if the game has been won.This function has 
    two parameters: the data structure representing the stock and the 
    data structure representing the tableau.'''

    ace_count = 0
    rank_count = 0
    for col in tableau:
        for i in col:
            card = i
            rank = i.rank()
            rank_count+=rank
            if card.rank() == 1:
                ace_count += 1
    
    # if the stock is empty and the tableau only has 4 aces return true
    if len(stock)< 1 and ace_count == 4 and rank_count == 4:
        return True
    return False 

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():

    '''prompt the user to enter an option and return a representation of
    the option designed to facilitate subsequent processing. This function 
    takes no parameters. It prompts the user for an option and checks that the 
    input supplied by the user is of the form requested in the menu. If the input 
    is not of the required form, the function prints an error message (error in option) and returns an empty list. '''

    while True:

        user_input = input("\nInput an option (DFTRHQ): ")
        tokens = user_input.strip().split()

        # If user input is empty, print error and return an empty list
        if len(tokens) == 0:
            print("\nError in option: {}".format(user_input))
            return []

        # Extract the first token and convert it to lower case
        cmd = tokens[0].lower()

        # Handle the case for each option
        if cmd == "d":

            # If there are more tokens than expected, print error and return an empty list
            if len(tokens) > 1:
                print("\nError in option: {}".format(user_input))
                return []

            # Return the option as a list with a single element
            return ['D']

        elif cmd == "r":

            if len(tokens) > 1:
                print("\nError in option: {}".format(user_input))
                return []
            return ['R']


        elif cmd == "h":
            if len(tokens) > 1:
                print("\nError in option: {}".format(user_input))
                return []
            return ['H']

        elif cmd == "q":
            if len(tokens) > 1:
                print("\nError in option: {}".format(user_input))
                return []
            return ['Q']

        elif cmd == "f":

            # If there are not exactly two tokens, print error and return an empty list
            if len(tokens) != 2:
                print("\nError in option: {}".format(user_input))
                return []
            try:
                col = int(tokens[1]) - 1
            except ValueError:

                # If the second token cannot be converted to an integer, print error and return an empty list
                print("\nError in option: {}".format(user_input))
                return []
            if col not in range(4):

                # If the column is not a valid number (between 1 and 4), print error and return an empty list
                print("\nError in option: {}".format(user_input))
                return []

            # Return the option as a list with two elements
            return ['F', col]


        elif cmd == "t":
            # If there are not exactly three tokens, print error and return an empty list
            if len(tokens) != 3:
                print("\nError in option: {}".format(user_input))
                return []

            try:
                from_col = int(tokens[1]) - 1
                to_col = int(tokens[2]) - 1

            except ValueError:
                # If the second or third token cannot be converted to an integer, print error and return an empty list
                print("\nError in option: {}".format(user_input))
                return []

            if from_col not in range(4) or to_col not in range(4):
                # If either column is not a valid number (between 1 and 4), print error and return an empty list
                print("\nError in option: {}".format(user_input))
                return []

            # Return the option as a list with three elements
            return ['T', from_col, to_col]
        else:
            # If the command is not one of the valid options, print error and return an empty list
            print("\nError in option: {}".format(user_input))
            return []



        
def main():
    # print the rules of the game and the menu
    print(RULES)
    print(MENU)

    # initialize the game 
    game = init_game()

    # extract the data from the game
    deck = game[0]
    tableau = game[1]
    foundation = game[2]

    # display the start of the game
    display(deck, tableau, foundation)

    # call the option function to get options from the user
    option = get_option()

    # intitalize variable to check if option is valid
    option_valid = True

    # intialize variable to see if it the game should be displayed again
    display_game = False

    # while loop to conitinue until Q is inputted
    while option_valid == True:

        # if the option isnt valid dont display the game and reprompt at the end of the loop
        if option == []:
            display_game = False

        # if option is D deal 4 cards to the tableau and display the updated game
        elif option == ['D']:
            deal_to_tableau(tableau, deck)
            display_game = True
            
        elif option[0] == 'F' and len(option) == 2:
            col = option[1]
            move_to_foundation(tableau, foundation, col)
            display_game = True
        elif option[0] == 'T':
            letter, from_col, to_col = option
            move_within_tableau(tableau, from_col, to_col)
            display_game = True

        # restart the game and reinitialize the game
        elif option == ['R']:
            print("\n=========== Restarting: new game ============")
            print(RULES)
            print(MENU)
            deck, tableau, foundation = init_game()
            display_game = True

        # display the menu   
        elif option == ['H']:
            print(MENU)
            display_game = True

        # print goodbye message and end the game
        elif option == ['Q']:
            print("\nYou have chosen to quit.")
            option_valid = False
            break
        
        # check for win if the player wins print win message and end the game
        if check_for_win(tableau, deck):
            print("\nYou won!")
            break
        
        # if the game should be displayed display it
        if display_game == True:
            display(deck, tableau, foundation)
        
        # reprompt for an option
        option = get_option()


if __name__ == '__main__':
     main()
