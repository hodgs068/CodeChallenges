#python file 1
from random import shuffle

class Card:
    def __init__(self, cardVal, suite, absCardValue, min, max):
        self.cardVal = cardVal
        self.suite = suite
        self.absCardValue = absCardValue
        self.min = min
        self.max = max

def val(absCardValue):
    cardVal = absCardValue % 13
    if cardVal == 0:
        cardVal = 13
    suite = (absCardValue - 1) // 13
    if cardVal == 13 or cardVal == 12 or cardVal == 11:
        min = 10
        max = 10
    elif cardVal == 1:
        min = 1
        max = 11 
    else:
        min = cardVal
        max = cardVal
    cardObj = Card(cardVal, suite, absCardValue, min, max)
    return cardObj

def printCardsShort(deckOrHand, hideFirstCard):
    tmpList = []
    for index, c in enumerate(deckOrHand):
        if hideFirstCard and index == 0:
            tmpList.append("**")
        else:
            if c.cardVal == 13:
                tmpList.append("K")
            elif c.cardVal == 12:
                tmpList.append("Q")
            elif c.cardVal == 11:
                tmpList.append("J")
            elif c.cardVal == 1:
                tmpList.append("A")
            else:
                tmpList.append(c.cardVal)                                                            
    print(f"Cards: {tmpList}")
    if isBust(deckOrHand):
        print("BUSTED!!!!!!!!!!!!!!!!!!!!!!!")
    if not hideFirstCard:
        print(f"\nHighest Good Hand: {idealHandValue(deckOrHand)}")
        print(f"Minimum Hand: {minHandTotal(deckOrHand)}")

def printGameStateShort(p1, p2, d, p1Turn, hideFirstDealerCard, wallet, bet, doubledDown):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    newCursor = "  <------------------"
    p1cursor = ""
    p2cursor = ""
    if p1Turn:
        p1cursor = newCursor
    else:
        p2cursor = newCursor
    print("***********************************************")
    print(f"Player1:{p1cursor}")
    printCardsShort(p1, False)
    print(f"\nWallet: ${wallet} Bet: ${bet} DoubledDown:{doubledDown}")
    print("-------------------------")
    print(f"Dealer:{p2cursor}")
    if hideFirstDealerCard:
        printCardsShort(p2, True)
    else:
        printCardsShort(p2, False)
    print("-------------------------")
    print("*****************************")


def minHandTotal(hand):
    total = 0
    for c in hand:
        total += c.min
    return total

def isBust(hand):
    busted = False
    if minHandTotal(hand) > 21:
        busted = True
    return busted

def handHasAce(hand):
    hasAce = False
    for c in hand:
        if c.cardVal == 1:
            hasAce = True
            break
    return hasAce

def idealHandValue(hand):
    value = minHandTotal(hand)
    if handHasAce(hand) and value + 10 <= 21:
        value += 10 # boost the value of one ace from 1 to 11 if it won't bust
    return value

def gameLoop(wallet, betInput):
    bet = betInput # default bet?
    winLossMultiplier = 0
    blackJackMultiplier = 1
    playerFolds = False
    doubledDown = False

    #setup deck
    deckRange = list(range(1,53))

    d = []  #deck of card objects
    for c in deckRange:
        d.append(val(c))
    shuffle(d)

    #setup players
    p1 = []
    p2 = []

    #set up initial state before game loop:
    p1Turn = True
    #deal 2 cards to each player, remove cards from main deck
    p1.append(d.pop())
    p1.append(d.pop())

    p2.append(d.pop())
    p2.append(d.pop())

    currentHand = p1
    #game loop:
    printGameStateShort(p1, p2, d, p1Turn, True, wallet, bet, doubledDown)
    while True:
        if p1Turn: # is p1 turn
            currentHand = p1
            #give choice to double down, or fold, but only on initial hand; if the player STAYS at 2 cards it should skip this part
            if len(currentHand) == 2:
                userInput = ""
                while True:
                    userInput = input("\nEnter 'd' to double down, 'f' to fold, any other key to continue:")
                    if userInput in ["d", "D"] and bet * 2 > wallet:
                        print("\nYou don't have enough cash to double down!!\n")
                        continue
                    else:
                        break
                if userInput in ["D","d"]: #handle doubling down, skip rest of p1's turn if they doubled down
                    bet *= 2
                    p1Turn = False
                    doubledDown = True
                    currentHand.append(d.pop())
                    if isBust(currentHand): #end game if double down busts
                        break
                    printGameStateShort(p1, p2, d, p1Turn, True, wallet, bet, doubledDown)
                    continue
                elif userInput in ["F", "f"]: #player folds, gets half their bet back, forfeits
                    bet = bet / 2
                    playerFolds = True
                    winLossMultiplier = -1
                    break
                else:
                    printGameStateShort(p1, p2, d, p1Turn, True, wallet, bet, doubledDown)
        else: #is p2 turn
            currentHand = p2
        userChoice = ""
        if p1Turn:
            while True:
                print("type H for hit, S for stay")
                userChoice = input("")
                if userChoice in ["h", "H", "s", "S"]: #validate input
                    break
        if not p1Turn:
            if idealHandValue(currentHand) >= 17: # Dealer behavior: don't hit if they have 17 points of ideal hand value
                userChoice = "s"
                print("(Dealer chooses STAY, press any key to continue)")
            else:
                userChoice = "h"
                print("(Dealer chooses HIT, press any key to continue)")
            input("")
        if userChoice in ["H", "h"]: #add extra card if player hits, test if they busted
            currentHand.append(d.pop())
            printGameStateShort(p1, p2, d, p1Turn, True, wallet, bet, doubledDown) # don't want to show game state after each computer dealer's choice
            if isBust(currentHand):
                break
            continue
        else:
            if isBust(currentHand): # test bust condition after player or dealer hits
                break
        #end of turn
        #switch the current player to prepare for next turn
        if p1Turn:
            p1Turn = False
        else:
            break
        printGameStateShort(p1, p2, d, p1Turn, True, wallet, bet, doubledDown)

    #detect final state
    printGameStateShort(p1, p2, d, p1Turn, False, wallet, bet, doubledDown)

    if not playerFolds: #full game was played:
        if not isBust(p1) and not isBust(p2):
            if idealHandValue(p1) == idealHandValue(p2):
                print("\n\n ------ Draw!! ------ \n\n")
                winLossMultiplier = 0
            elif idealHandValue(p1) > idealHandValue(p2):
                print("\n\n ------ You Won!! ------ \n\n")
                winLossMultiplier = 1
                if idealHandValue(p1) == 21:
                    blackJackMultiplier = 1.5
                    print("BLACK JACK! Winnings increased by 50 Percent!!")             
            else:
                print("\n\n ------ Dealer Wins, You Lose!! ------ \n\n")
                winLossMultiplier = -1
        elif (isBust(p1) and isBust(p2)):
            print("\n\n ------ Draw!! ------ \n\n")
            winLossMultiplier = 0
        elif isBust(p2):
            print("\n\n ------ You Won!! ------ \n\n")
            winLossMultiplier = 1
            if idealHandValue(p1) == 21:
                blackJackMultiplier = 1.5
                print("BLACK JACK! Winnings increased by 50 Percent!!") 
        else:
            print("\n\n ------ Dealer Wins, You Lose!! ------ \n\n")
            winLossMultiplier = -1        
    else:  #player folded on first turn
        print("\n\n ------ You Folded, you receive back half your bet!! ------ \n\n")

    winnings = bet * blackJackMultiplier * winLossMultiplier
    wallet += winnings
    if winnings < 0:
        print(f"You lost ${winnings} this round")
    else:
        print(f"Your winnings this round are {winnings}")
    return wallet

def main():
    wallet = 100
    while True:
        #get initial bet before game
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYour wallet value is ${wallet}\n")
        while True:
            try:
                betInput = int(input("Please enter your initial bet, or press any key to use default $10 bet:"))
            except:
                betInput = 10
            #
            if betInput > wallet:
                print("\nYou cannot bet more than your wallet amount!\n")
                continue
            elif betInput < 10:
                print("\nMinimum bet is $10, cheapwad!!   >:(  \n")
                continue
            break
        wallet = gameLoop(wallet, betInput)
        #print()
        print(f"\nYour current wallet value is ${wallet}\n")
        if wallet <= 0:
            print("You are out of Money, please leave the Casino :( ")
            break
        elif wallet >= 200:
            print("You are are now wealthy; you can retire in style! :)  ")
            break            
        while True:
            userInput = input("Would you like to play another game? press 'Y' for yes, 'N' for no\n")
            if userInput in ["Y","y"]:
                break
            elif userInput in ["N","n"]:
                print(f"\n\n\n\nYou left the casino with ${wallet} in your pocket.  Come again soon!\n")
                return

main()