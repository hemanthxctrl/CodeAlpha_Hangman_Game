import random

# Predefined word list
words = ["python", "laptop", "gaming", "coding", "market"]

# Select a random word
word = random.choice(words)
guessed_word = ["_"] * len(word)

# Game variables
guessed_letters = []
incorrect_guesses = 0
max_attempts = 6

print("🎮 Welcome to Hangman!")
print("Guess the word letter by letter.")

# Game loop
while incorrect_guesses < max_attempts and "_" in guessed_word:
    print("\nWord:", " ".join(guessed_word))
    print("Guessed Letters:", guessed_letters)
    print(f"Attempts Left: {max_attempts - incorrect_guesses}")

    guess = input("Enter a letter: ").lower()

    # Validate input
    if len(guess) != 1 or not guess.isalpha():
        print("❌ Please enter a single valid letter.")
        continue

    if guess in guessed_letters:
        print("⚠️ You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    # Check guess
    if guess in word:
        print("✅ Correct!")
        for i in range(len(word)):
            if word[i] == guess:
                guessed_word[i] = guess
    else:
        print("❌ Wrong!")
        incorrect_guesses += 1

# Game result
if "_" not in guessed_word:
    print("\n🎉 You won! The word was:", word)
else:
    print("\n💀 You lost! The word was:", word)