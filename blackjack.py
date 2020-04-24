# Black Jack game for group James Dwyer, Andre Medeiros, Elton Dias,
# Rony Lopes, Ryan Thomas, Demeus Alves, Sourivong Thepsimoung

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


def blackjack_or_bust(hand):
    if hand == 21:
        print("Winner")
        quit()
    elif hand > 21:
        return True
    else:
        return False


'''
# check if current hand is busted
def bust_check(hand) -> bool:
    if hand > 21:
        return True
    else:
        return False
'''

# dealer action
def dealer_actions(dealers_hand, dealers_hand_value, stack):
    while (dealers_hand_value < 17):
        dealers_hand.add(stack.deal(1))
        dealers_hand_value = sum_of_card(dealers_hand)
    print("The dealers hand is now:\n", dealers_hand)
    print("The dealers hand value is now:\n", dealers_hand_value)
    return dealers_hand_value

def main():
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
    print("The value of the players hand is ", players_hand_value)

    print("\n", "Dealer hand is:\n", dealer_hand[1])
    dealer_hand_value = sum_of_card(dealer_hand)

    # Black Jack Check
    blackjack_or_bust(players_hand_value)

    # Check here for dealers 21 because if it has 21 we need to print out dealers value and cards as well
    if dealer_hand_value == 21:
        print("Dealer wins the hand")
        print("The dealers cards are", dealer_hand)
        print("The dealers value is", dealer_hand_value)

    # loop to play the game

    pick_action = input("\nWould you like to hit ('h'), stand ('s') or double down ('d'): ").lower()

    while pick_action != 'q':

        if pick_action == 'h':

            # create hit function instead so we can pass in whoevers turn it is
            players_hand.add(stack.deal(1))
            players_hand_value = sum_of_card(players_hand)
            print(players_hand)
            print("\n The value of the hand is ", players_hand_value)
            blackjack_or_bust(players_hand_value)

            # hand_value = add_card(players_hand, stack)

            # check the cards value
            if blackjack_or_bust(players_hand_value) == True:
                print("Player has busted")
                return
            else:
                pick_action = input("\nWould you like to hit ('h'), stand ('s') or double down ('d'): ").lower()

        elif pick_action == 'q':
            sys.quit()

        elif pick_action == 's':
            if players_hand_value < 17 and dealer_hand_value >= 17:
                print("You lose")
                return
            else:
                dealer_hand_value = dealer_actions(dealer_hand, dealer_hand_value, stack)
                if blackjack_or_bust(dealer_hand_value) == True:
                    print("Dealer has busted")
                    return

                if (dealer_hand_value > players_hand_value):
                    print("Dealer wins")

                elif (players_hand_value > dealer_hand_value):
                    print("Player wins")

                elif (dealer_hand_value == players_hand_value):
                    print("The hand is Pushed")

                return

if __name__ == "__main__":
    main()
