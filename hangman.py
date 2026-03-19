import random


WORDS = ["python", "keyboard", "algorithm", "variable", "function"]


HANGMAN_STAGES = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
]

MAX_WRONG = 6


def display_word(word: str, guessed: set) -> str:
    """Return the word with unguessed letters shown as underscores."""
    return " ".join(letter if letter in guessed else "_" for letter in word)


def play():
    word = random.choice(WORDS)
    guessed: set = set()
    wrong_letters: list = []

    print("\n" + "=" * 40)
    print("       W E L C O M E   T O   H A N G M A N")
    print("=" * 40)

    while True:
        # ── Draw current gallows state ─────────────────────────────────────────
        print(HANGMAN_STAGES[len(wrong_letters)])
        print(f"  Word  : {display_word(word, guessed)}")
        print(f"  Wrong : {', '.join(wrong_letters) if wrong_letters else '—'}")
        print(f"  Guesses left: {MAX_WRONG - len(wrong_letters)}\n")

        # ── Check win ─────────────────────────────────────────────────────────
        if all(letter in guessed for letter in word):
            print(f"  🎉  You won! The word was '{word}'.")
            break

        # ── Check loss ────────────────────────────────────────────────────────
        if len(wrong_letters) >= MAX_WRONG:
            print(f"  💀  You lost! The word was '{word}'.")
            break

        # ── Get player input ──────────────────────────────────────────────────
        guess = input("  Guess a letter: ").strip().lower()

        if not guess or not guess.isalpha() or len(guess) != 1:
            print("  ⚠  Please enter a single letter.\n")
            continue

        if guess in guessed or guess in wrong_letters:
            print(f"  ⚠  You already guessed '{guess}'.\n")
            continue

        # ── Evaluate guess ────────────────────────────────────────────────────
        if guess in word:
            guessed.add(guess)
            print(f"  ✓  Good guess!\n")
        else:
            wrong_letters.append(guess)
            print(f"  ✗  Wrong!\n")

    # ── Play again? ────────────────────────────────────────────────────────────
    again = input("\n  Play again? (y/n): ").strip().lower()
    if again == "y":
        play()
    else:
        print("\n  Thanks for playing! Goodbye.\n")


if __name__ == "__main__":
    play()