from random import shuffle

pot = 0

deck = [str(x) for x in range(1,11)] + ['10']*3
deck = deck*4
shuffle(deck)

def resetDeck():
    global deck
    deck = [str(x) for x in range(1,11)] + ['10']*3
    deck = deck*4
    shuffle(deck)

def getCard(person):
    nextCard = deck.pop()
    print(person + '\'s Card:' + str(nextCard))
    return nextCard

class Player:
    def __init__(self, name, wallet, cards=[]):
        self.name = name
        self.wallet = wallet
        self.cards = cards
        self.bet = 0

    def returnSum(self):
        return sum(list(map(int,self.cards)))

    def returnBet(self):
        return self.bet

    def printMe(self):
        return self.name + '\'s CARDS:' + ' '.join(self.cards)

    def placeBet(self, amount):
        global pot
        if amount > self.wallet:
            print('Ops! You don\'t seem to have enough cash')
        elif amount == self.wallet:
            c = input('Are you sure you want to go ALL-IN?(y/n)')
            if c == 'y':
                self.wallet -= amount
                self.bet += amount
                pot += amount
                print('CASH:' + str(self.wallet))
        else:
            self.wallet -= amount
            self.bet += amount
            pot += amount
            print('CASH-REMAINING:' + str(self.wallet))

    def hit(self):
        print('Hitting once')
        card = getCard(self.name)
        self.cards.append(card)

    def oneTOeleven(self):
        print('ONE TO ELEVEN')
        if '1' not in self.cards:
            print('No 1s to convert')
        else:
            more = 'y'
            while '1' in self.cards and more == 'y':
                self.cards[self.cards.index('1')] = '11'
                print(player.printMe())
                more = input('Convert more y/n? (If present)')

    def elevenTOone(self):
        print('ELEVEN TO ONE')
        if '11' not in self.cards:
            print('No 11s to convert')
        else:
            more = 'y'
            while '11' in self.cards and more == 'y':
                self.cards[self.cards.index('11')] = '1'
                print(player.printMe())
                more = input('Convert more y/n? (If present)')

    def reset(self):
        self.bet = 0
        self.cards = []


class Dealer:
    def __init__(self):
        print('WELCOME TO BLACKJACK!')
        self.cards = []

    def initialize(self, other):
        print('Initializing Table')
        other.cards.append(getCard(other.name))
        self.cards.append(getCard('Dealer'))
        other.cards.append(getCard(other.name))

    def stand(self):
        print('CPU playing')
        while sum(list(map(int,self.cards))) < 17:
            self.cards.append(getCard('Dealer'))

    def printMe(self):
        return 'DEALER\'s CARDS:' + ' '.join(self.cards)

    def returnSum(self):
        return sum(list(map(int,self.cards)))

    def reset(self):
        self.cards = []



def compare(a,b):
    if a <= 21 and (b < a or b > 21):
        return 'D'
    elif b <= 21 and (a < b or a > 21):
        return 'P'
    else:
        return 'DR'



dealer = Dealer()
reset = True
while reset:
    pot = 0
    name = input('Please Enter Your name:')
    while True:
        wallet = int(input('Enter the amount of cash you have:'))
        if wallet < 1000 or wallet > 10000:
            print('Please enter an amount in the range of 1000 and 10000')
            continue
        else:
            break
    player = Player(name, wallet)
    newGame = 'y'
    while newGame == 'y':
        if player.wallet <= 0:
            print('You are out of CASH!')
            break
        resetDeck()
        pot = 0
        while pot == 0:
            amount = int(input('BET:'))
            player.placeBet(amount)
        dealer.initialize(player)
        print(dealer.printMe() + ' | ' + player.printMe())
        gameOver = False
        winner = None
        while not gameOver:
            choice = int(input('''
                Enter your choice:\n
                1. HIT\n
                2. STAND\n
                3. DOUBLE\n
                4. SURRENDER\n
                5. Change 1 to 11\n
                6. Change 11 to 1\n
            '''))

            if choice == 1:
                player.hit()
            elif choice == 2:
                dealer.stand()
                winner = compare(dealer.returnSum(), player.returnSum())
                gameOver = True
            elif choice == 3:
                if len(player.cards) > 2:
                    print('Cannot play double after a HIT')
                    continue
                if player.returnBet() > player.wallet:
                    print('You do not have enough cash to play DOUBLE')
                    continue
                print('Playing Double')
                player.placeBet(player.returnBet())
                player.hit()
                if player.returnSum() > 21:
                    winner = 'D'
                    gameOver = True
                else:
                    changes = input('Convert 1 to 11? (y/n)')
                    if changes == 'y':
                        player.oneTOeleven()
                    changes = input('Convert 11 to 1? (y/n)')
                    if changes == 'y':
                        player.elevenTOone()
                    dealer.stand()
                    winner = compare(dealer.returnSum(), player.returnSum())
                    gameOver = True
            elif choice == 4:
                print('Surrendering')
                winner = 'DR'
                pot -= pot//2
                gameOver = True
            elif choice == 5:
                player.oneTOeleven()
            elif choice == 6:
                player.elevenTOone()
            else:
                print('INVALID CHOICE!')
                continue
            print(dealer.printMe() + ' | ' + player.printMe() + ' | POT:' + str(pot) + ' | BET:' + str(player.bet))
            if player.returnSum() == 21:
                pot *= 1.5
                winner = 'P'
                gameOver = True
            if player.returnSum() > 21:
                winner = 'D'
                gameOver = True
            if gameOver == True:
                if winner == 'D':
                    print('YOU LOSE!\nWALLET - {}'.format(pot))
                    print('WALLET:{}'.format(player.wallet))
                    pot = 0
                elif winner == 'P':
                    player.wallet += pot*2

                    print('YOU WIN!')
                    print('WALLET + {}'.format(pot))
                    print('WALLET:{}'.format(player.wallet))
                    pot = 0
                else:
                    player.wallet += pot
                    print('PUSH!')
                    print('WALLET - {}'.format(pot))
                    print('WALLET:{}'.format(player.wallet))
                    pot = 0
        dealer.reset()
        player.reset()
        newGame = input('Another Game? (y/n)')
    c = int(input('1. QUIT\n2. RESET WALLET and RESTART\n'))
    if c == 1:
        reset = False
    else:
        dealer.reset()
        player.reset()
