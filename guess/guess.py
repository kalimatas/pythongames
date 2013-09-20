import random
print('Guess the number game', end='\n\n')

print('Name: ', end='')
name = input()
number = random.randint(1, 20)
taken = 0

print('Number is between 1 and 20.');
while taken < 6:
    print('Take a guess: ', end='')
    guess = input()
    guess = int(guess)
    taken += 1

    if guess < number:
        print('Too low')

    if guess > number:
        print('Too high')

    if guess == number:
        break

if guess == number:
    print('You guessed number ' + str(number) + ' in ' + str(taken) + ' guesses!')
else:
    print('Nope. The number was: ' + str(number))
