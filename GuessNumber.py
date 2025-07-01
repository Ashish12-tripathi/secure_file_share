import random

print("Welcome to my Guess the Number Game!")
print("You have only 4 chances to guess the number between 1 and 100.")

number = random.randint(1, 100)
attempts = 0
max_attempts = 4

while attempts < max_attempts:
    guess = input(f"Attempt {attempts + 1} of {max_attempts} - Enter your guess: ")

    if not guess.isdigit():
        print("Please enter a valid number!")
        continue

    guess = int(guess)
    attempts += 1

    if guess < number:
        print("Too low!")
    elif guess > number:
        print("Too high!")
    else:
        print(f"🎉 Congratulations! You guessed it in {attempts} attempts.")
        break
else:
    print(f"😞 Sorry, you lost! The correct number was {number}. Better luck next time!")
