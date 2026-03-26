import random

words = ["python", "laptop", "gaming", "coding", "market"]

# Select random word
word = random.choice(words)
guessed_word = ["_"] * len(word)

guessed_letters = []

# 🎚️ Difficulty selection
print("🎮 Welcome to Hangman!")
print("Select Difficulty: Easy / Medium / Hard")

difficulty = input("Enter difficulty: ").lower()

if difficulty == "easy":
    max_attempts = 8
elif difficulty == "hard":
    max_attempts = 4
else:
    max_attempts = 6  # default = medium

incorrect_guesses = 0

# 💡 Hint: reveal one random letter

hint_letter = random.choice(word)
print(f"\n💡 Hint: The word contains the letter '{hint_letter}'")

for i in range(len(word)):
    if word[i] == hint_letter:
        guessed_word[i] = hint_letter

# 🎯 Game loop

while incorrect_guesses < max_attempts and "_" in guessed_word:
    print("\nWord:", " ".join(guessed_word))
    print("Guessed Letters:", guessed_letters)
    print(f"Attempts Left: {max_attempts - incorrect_guesses}")

    guess = input("Enter a letter: ").lower()

    # Input validation
    if len(guess) != 1 or not guess.isalpha():
        print("❌ Enter a single valid letter.")
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

# 🏁 Result
if "_" not in guessed_word:
    print("\n🎉 You won! The word was:", word)
else:
    print("\n💀 You lost! The word was:", word)