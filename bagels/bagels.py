#!/usr/bin/env python

NUMBERS = 3
MAXGUESSES = 10

def getSecretNum(numDigits):
    """
    @numDigits: int
    """
    import random
    numbers = list(range(10))
    random.shuffle(numbers)
    secretNum = ''
    for i in range(numDigits):
        secretNum += str(numbers[i])
    return secretNum

def getClues(guess, secretNum):
    if guess == secretNum:
        return 'You got it!'

    clue = []
    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            clue.append('Fermi')
        elif guess[i] in secretNum:
            clue.append('Pico')
    if len(clue) == 0:
        return 'Bagels'

    clue.sort()
    return ' '.join(clue)

def playAgain():
    print("Do you want to play again? (yes or no)")
    return input().lower().startswith('y')

def isOnlyDigits(num):
    num = str(num)
    return num.isdigit()

if __name__ == "__main__":
    print("%s-digit number. Try to guess." % (NUMBERS))
    while True:
        secretNum = getSecretNum(NUMBERS)
        print('You have %s guesses to get the number.' % (MAXGUESSES))

        numGuesses = 1
        while numGuesses <= MAXGUESSES:
            guess = ''
            while len(guess) != NUMBERS or not isOnlyDigits(guess):
                print('Guess #%s: ' % (numGuesses))
                guess = input()

            clue = getClues(guess, secretNum)
            print(clue)
            numGuesses += 1

            if guess == secretNum:
                break
            if numGuesses > MAXGUESSES:
                print('You ran out of guesses. The answer was %s.' % (secretNum))
        if not playAgain():
            break
         
    
    
