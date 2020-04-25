

# pygame and pydealer
# import pygame
import pydealer
from stack import Stack
from pydealer.const import POKER_RANKS
import sys


# initialize the pygame library
# pygame.init()


# actions class to handle all of our player actions for the game
class Actions:
    def __init__(self, hit, split, double_down, stay, bet, deal, total):
        self.hit = hit
        self.split = split
        self.double_down = double_down
        self.stay = stay
        self.bet = bet
        self.deal = deal
        self.total = total
        return


# money class to keep track of player earnings
class Money:
    def __init__(self, total, add, subtract):
        self.total = total
        self.add = add
        self.subtract = subtract
'''
This function takes in the strings of the two cards in the user and dealers hands. It determines if it is a face card,
ace, or just a normal number and computes the two cards values together to create hand values.

hand: string representations of the cards
'''
def sum_of_card(hand):
    sum = 0
    for card in hand:
        if card.value not in ('Jack', 'Queen', 'King', 'Ace'):
            sum = sum + int(card.value)
        elif card.value in ('Jack', 'Queen', 'King'):
            sum = sum + 10
        elif sum < 11 and card.value in ('Ace'):
            sum = sum + 11
        elif sum >= 11 and card.value in ('Ace'):
            sum = sum + 1
    # print("\n The value of the hand is ", sum)
    return sum

'''
This function computes if the player or dealer first has blackjack, if not we are also passing in a hand when there is a chance a hand could be busted.

hand: player or dealers hand value
'''
def blackjack_or_bust(hand):
    if hand == 21:
        print("Winner")
        play_again = input("\nDo you want to play again: 'y' or 'n':\n").lower()
        if play_again == 'y':
            game()
    elif hand > 21:
        return

'''
This function is called after the user decides they want to stand. A dealer must hit until they have a value of at least 17.

dealers hand: holds the cards strings representation
dealers hand value: int of hands value
stack: current stack that is being used to add cards from
'''
def dealer_actions(dealers_hand, dealers_hand_value, stack):
    while (dealers_hand_value < 17):
        dealers_hand.add(stack.deal(1))
        dealers_hand_value = sum_of_card(dealers_hand)
    print("\nThe dealers hand is now:\n", dealers_hand)
    print("\nValue =", dealers_hand_value)
    return dealers_hand_value

def game():
    stack = pydealer.Stack()  # creating stack variable and = to pydealers stack
    deck = pydealer.Deck(rank=POKER_RANKS, rebuild=True,
                         re_shuffle=True)  # creating deck variable and = to pydealers deck of 52 cards
    stack.add(deck)  # Adds 52 cards to the deck
    stack.shuffle()  # Shuffles deck
    Stack.is_sorted(deck)

    players_hand = pydealer.Stack()
    dealer_hand = pydealer.Stack()
    players_hand.add((stack.deal(2)))  # Adding two cards to the players hand
    dealer_hand.add((stack.deal(2)))

    print("Players hand is:\n", players_hand)
    players_hand_value = sum_of_card(players_hand)  # function returns sum which contains the value
    print("Value =", players_hand_value)

    dealer_hand_value = sum_of_card(dealer_hand)
    if dealer_hand_value == 21:
        print("\nDealer wins the hand\n")
        print(dealer_hand)
        print("Value:", dealer_hand_value)
        return
    print("\n", "Dealer hand is:\n", dealer_hand[1])

    # Black Jack Check
    blackjack_or_bust(players_hand_value)

    pick_action = input("\nWould you like to hit ('h'), stand ('s') or double down ('d'): ").lower()

    while pick_action != 'q':

        if pick_action == 'h':

            players_hand.add(stack.deal(1))
            players_hand_value = sum_of_card(players_hand)
            print(players_hand)
            print("\n The value of the hand is ", players_hand_value)
            blackjack_or_bust(players_hand_value)

            if blackjack_or_bust(players_hand_value) == True:
                print("Player has busted")
                return
            else:
                pick_action = input("\nWould you like to hit ('h'), stand ('s') or double down ('d'): ").lower()
        elif pick_action == 'q':
            sys.exit()
        elif pick_action == 's':
            if players_hand_value < 17 and dealer_hand_value >= 17:
                print("\nThe dealers hand is now:\n", dealer_hand)
                print("\nValue =", dealer_hand_value)
                print("You lose")
                return
            else:
                dealer_hand_value = dealer_actions(dealer_hand, dealer_hand_value, stack)
                if blackjack_or_bust(dealer_hand_value) == True:
                    print("\nDealer has busted")
                    return

                if (dealer_hand_value > players_hand_value):
                    print("\nDealer wins")
                elif (players_hand_value > dealer_hand_value):
                    print("\nPlayer wins")
                elif (dealer_hand_value == players_hand_value):
                    print("\nThe hand is Pushed")
                return




def main():
    game()
    play_again = input("\nDo you want to play again: 'y' or 'n':\n").lower()
    while(play_again != "n"):
        game()
        play_again = input("\nDo you want to play again: 'y' or 'n':\n").lower()

    return




if __name__ == "__main__":
    main()
