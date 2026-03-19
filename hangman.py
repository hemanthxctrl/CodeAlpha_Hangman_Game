import random

# ── Word bank: category → difficulty → list of (word, hint) ───────────────────
WORD_DATA = {
    "animals": {
        "easy":   [("cat","meows"),("dog","barks"),("fish","swims"),("bird","flies"),("bear","hibernates")],
        "medium": [("elephant","largest land animal"),("dolphin","smart ocean mammal"),("penguin","flightless antarctic bird"),("giraffe","tallest animal"),("leopard","spotted big cat")],
        "hard":   [("chameleon","changes color"),("platypus","egg-laying mammal"),("axolotl","regenerates limbs"),("narwhal","unicorn of the sea"),("wolverine","fierce mustelid")],
    },
    "countries": {
        "easy":   [("india","largest democracy"),("china","most populous"),("japan","land of the rising sun"),("france","home of the eiffel tower"),("brazil","amazon rainforest")],
        "medium": [("germany","central europe"),("mexico","north of central america"),("nigeria","most populous african nation"),("turkey","bridges europe and asia"),("vietnam","southeast asian country")],
        "hard":   [("mozambique","southeastern africa"),("azerbaijan","caucasus region"),("kyrgyzstan","central asia"),("madagascar","large island off africa"),("luxembourg","tiny european country")],
    },
    "tech": {
        "easy":   [("loop","repeat code"),("array","list of items"),("class","object blueprint"),("debug","fix errors"),("input","data from user")],
        "medium": [("python","popular language"),("variable","stores a value"),("function","reusable code block"),("boolean","true or false"),("integer","whole number type")],
        "hard":   [("algorithm","steps to solve a problem"),("recursion","function calls itself"),("inheritance","oop concept"),("polymorphism","many forms"),("asynchronous","non-blocking execution")],
    },
    "science": {
        "easy":   [("atom","smallest unit of matter"),("cell","basic unit of life"),("wave","energy transfer"),("gene","unit of heredity"),("mass","amount of matter")],
        "medium": [("gravity","pulls objects together"),("nucleus","center of an atom"),("protein","made of amino acids"),("neutron","neutral atomic particle"),("climate","long-term weather patterns")],
        "hard":   [("photosynthesis","plants make food from light"),("chromosome","carries genetic info"),("thermodynamics","study of heat and energy"),("mitochondria","powerhouse of the cell"),("equilibrium","balanced state")],
    },
}

# ── Gallows ASCII art (index = wrong-guess count) ─────────────────────────────
STAGES = [
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

# ── Difficulty settings ────────────────────────────────────────────────────────
DIFF_CONFIG = {
    "easy":   {"max_wrong": 8, "hints": 3, "points": 10},
    "medium": {"max_wrong": 6, "hints": 2, "points": 20},
    "hard":   {"max_wrong": 5, "hints": 1, "points": 35},
}

CATEGORIES = list(WORD_DATA.keys())
DIFFICULTIES = list(DIFF_CONFIG.keys())


# ── Helpers ───────────────────────────────────────────────────────────────────
def display_word(word: str, guessed: set) -> str:
    return "  " + "  ".join(c if c in guessed else "_" for c in word)


def choose_option(prompt: str, options: list) -> str:
    print(f"\n{prompt}")
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        raw = input("  Your choice (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("  Invalid choice — try again.")


def header(title: str):
    print("\n" + "=" * 44)
    print(f"  {title}")
    print("=" * 44)


# ── Core game ─────────────────────────────────────────────────────────────────
def play_round(category: str, difficulty: str, session: dict) -> bool:
    cfg = DIFF_CONFIG[difficulty]
    max_wrong = cfg["max_wrong"]
    hints_left = cfg["hints"]
    point_value = cfg["points"]

    pool = WORD_DATA[category][difficulty]
    word, hint = random.choice(pool)

    guessed: set = set()
    wrong_letters: list = []

    while True:
        # ── Draw stage ────────────────────────────────────────────────────────
        stage_idx = min(len(wrong_letters), len(STAGES) - 1)
        print(STAGES[stage_idx])
        print(f"  Category   : {category}  |  Difficulty : {difficulty}")
        print(f"  Score      : {session['score']}  pts")
        print(f"  Wins       : {session['wins']}   |  Streak : {session['streak']}")
        print()
        print(f"  Word  : {display_word(word, guessed)}")
        print(f"  Wrong : {', '.join(wrong_letters) if wrong_letters else '—'}")
        print(f"  Guesses left : {max_wrong - len(wrong_letters)} / {max_wrong}")
        print(f"  Hints left   : {hints_left}")
        print()

        # ── Win / loss check ──────────────────────────────────────────────────
        won = all(c in guessed for c in word)
        lost = len(wrong_letters) >= max_wrong

        if won:
            earned = max(point_value - len(wrong_letters) * 2, point_value // 2)
            session["score"] += earned
            session["wins"] += 1
            session["streak"] += 1
            print(f"  ✓  You got it! The word was '{word}'.")
            print(f"  +{earned} points!  Streak: {session['streak']}")
            return True

        if lost:
            session["streak"] = 0
            print(f"  ✗  Game over! The word was '{word}'.")
            return False

        # ── Player input ──────────────────────────────────────────────────────
        print("  Options: enter a letter, H = hint, Q = quit round")
        raw = input("  > ").strip().lower()

        if raw == "q":
            print("  Round skipped.")
            session["streak"] = 0
            return False

        if raw == "h":
            if hints_left <= 0:
                print("  No hints remaining!")
                continue
            unguessed = [c for c in word if c not in guessed]
            if not unguessed:
                continue
            reveal = random.choice(unguessed)
            guessed.add(reveal)
            hints_left -= 1
            print(f"  Hint: the letter '{reveal}' is in the word.")
            continue

        if raw == "?":
            print(f"  Hint text: {hint}")
            continue

        if not raw or not raw.isalpha() or len(raw) != 1:
            print("  Please enter a single letter (or H for hint, ? for clue).")
            continue

        if raw in guessed or raw in wrong_letters:
            print(f"  You already guessed '{raw}'.")
            continue

        if raw in word:
            guessed.add(raw)
            print(f"  '{raw}' is in the word!")
        else:
            wrong_letters.append(raw)
            print(f"  '{raw}' is not in the word.")


# ── Session loop ──────────────────────────────────────────────────────────────
def main():
    session = {"score": 0, "wins": 0, "streak": 0}

    header("HANGMAN  v2")
    print("  Type '?' during a round to reveal the hint text.")
    print("  Type 'H' during a round to use a hint (reveals a letter).")

    category   = choose_option("Choose a category:", CATEGORIES)
    difficulty = choose_option("Choose difficulty:", DIFFICULTIES)

    while True:
        play_round(category, difficulty, session)

        header("ROUND OVER")
        print(f"  Total score : {session['score']}")
        print(f"  Total wins  : {session['wins']}")
        print(f"  Streak      : {session['streak']}")

        again = input("\n  Play again? (y = same settings, n = change, q = quit): ").strip().lower()
        if again == "q":
            break
        elif again == "n":
            category   = choose_option("Choose a category:", CATEGORIES)
            difficulty = choose_option("Choose difficulty:", DIFFICULTIES)
        # else continue with same settings

    header("THANKS FOR PLAYING")
    print(f"  Final score : {session['score']}")
    print(f"  Total wins  : {session['wins']}\n")


if __name__ == "__main__":
    main()