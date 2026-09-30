"""
Task 1: Basic Text-Based Game
Level 1: Beginner
Internship Program: Software Development - Cognifyz Technologies

Objective:
Implement a simple game using conditional statements for game logic.

Features:
- Game 1: Smart Number Guessing Game (with difficulty levels, score calculation, hints)
- Game 2: Software Development & Coding Trivia Quiz
- Interactive menu to select games, view rules, and play repeatedly
- Fully testable with programmatic and simulated input modes
"""

import random
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class NumberGuessingGame:
    """Number Guessing Game using conditional statements for game logic."""

    DIFFICULTIES = {
        "1": ("Easy (1 - 50, 10 attempts)", 1, 50, 10),
        "2": ("Medium (1 - 100, 7 attempts)", 1, 100, 7),
        "3": ("Hard (1 - 200, 5 attempts)", 1, 200, 5),
    }

    def __init__(self, difficulty="2"):
        name, low, high, max_attempts = self.DIFFICULTIES.get(
            difficulty, self.DIFFICULTIES["2"]
        )
        self.difficulty_name = name
        self.low = low
        self.high = high
        self.max_attempts = max_attempts
        self.secret_number = random.randint(self.low, self.high)
        self.attempts_used = 0
        self.is_won = False

    def evaluate_guess(self, guess: int) -> dict:
        """
        Evaluate a user's guess using conditional logic.
        Returns a dict with status, message, and hint.
        """
        self.attempts_used += 1

        if guess < self.low or guess > self.high:
            return {
                "status": "out_of_bounds",
                "message": f"Out of bounds! Guess must be between {self.low} and {self.high}.",
                "attempts_left": self.max_attempts - self.attempts_used,
            }

        diff = abs(self.secret_number - guess)

        if guess == self.secret_number:
            self.is_won = True
            score = max(10, (self.max_attempts - self.attempts_used + 1) * 20)
            return {
                "status": "correct",
                "message": f"🎉 Congratulations! You guessed the number {self.secret_number} in {self.attempts_used} attempts!",
                "score": score,
                "attempts_left": self.max_attempts - self.attempts_used,
            }
        elif guess < self.secret_number:
            hint = "Hot! Very close!" if diff <= 5 else ("Warm! Close!" if diff <= 15 else "Cold!")
            msg = f"📉 Too low! ({hint})"
        else:
            hint = "Hot! Very close!" if diff <= 5 else ("Warm! Close!" if diff <= 15 else "Cold!")
            msg = f"📈 Too high! ({hint})"

        attempts_left = self.max_attempts - self.attempts_used
        if attempts_left <= 0:
            return {
                "status": "game_over",
                "message": f"{msg}\n💥 Game Over! The secret number was {self.secret_number}.",
                "attempts_left": 0,
            }

        return {
            "status": "continue",
            "message": msg,
            "attempts_left": attempts_left,
        }

    def play_interactive(self):
        """Play the guessing game via standard input."""
        print("\n" + "=" * 50)
        print(f"🎮 Welcome to the Number Guessing Game!")
        print(f"Difficulty: {self.difficulty_name}")
        print(f"Rules: Guess the secret number between {self.low} and {self.high}.")
        print("=" * 50)

        while self.attempts_used < self.max_attempts and not self.is_won:
            prompt = f"\n[Attempt {self.attempts_used + 1}/{self.max_attempts}] Enter your guess: "
            try:
                user_input = input(prompt).strip()
                if user_input.lower() in ("q", "quit", "exit"):
                    print("Game exited by user.")
                    return
                guess = int(user_input)
            except ValueError:
                print("❌ Invalid input! Please enter an integer number.")
                continue

            result = self.evaluate_guess(guess)
            print(result["message"])
            if result["status"] in ("correct", "game_over"):
                if result.get("score"):
                    print(f"⭐ Your Final Score: {result['score']}/100")
                break


class TriviaQuizGame:
    """Software Development Trivia Quiz Game."""

    QUESTIONS = [
        {
            "question": "Which data structure operates on a First-In-First-Out (FIFO) basis?",
            "options": ["A. Stack", "B. Queue", "C. Tree", "D. Graph"],
            "answer": "B",
            "explanation": "A Queue follows the FIFO principle where the first element added is the first to be removed.",
        },
        {
            "question": "What is the time complexity of looking up a key in a Python dictionary on average?",
            "options": ["A. O(1)", "B. O(n)", "C. O(log n)", "D. O(n^2)"],
            "answer": "A",
            "explanation": "Python dictionaries are implemented using hash tables with average O(1) time complexity.",
        },
        {
            "question": "Which of the following is NOT an Object-Oriented Programming (OOP) pillar?",
            "options": ["A. Encapsulation", "B. Inheritance", "C. Compilation", "D. Polymorphism"],
            "answer": "C",
            "explanation": "The four main pillars of OOP are Encapsulation, Abstraction, Inheritance, and Polymorphism.",
        },
        {
            "question": "What does CRUD stand for in software engineering?",
            "options": [
                "A. Create, Read, Update, Delete",
                "B. Compile, Run, Undo, Debug",
                "C. Connect, Retrieve, Upload, Deploy",
                "D. Cache, Reset, Unload, Destroy",
            ],
            "answer": "A",
            "explanation": "CRUD refers to the four basic operations of persistent storage: Create, Read, Update, Delete.",
        },
        {
            "question": "Which keyword in Python is used to handle exceptions?",
            "options": ["A. catch", "B. except", "C. handle", "D. error"],
            "answer": "B",
            "explanation": "Python uses 'try...except' blocks for handling exceptions.",
        },
    ]

    def __init__(self):
        self.score = 0
        self.total_questions = len(self.QUESTIONS)

    def evaluate_answer(self, question_idx: int, user_answer: str) -> dict:
        """Evaluate the answer for a specific question."""
        q = self.QUESTIONS[question_idx]
        is_correct = user_answer.strip().upper() == q["answer"]
        if is_correct:
            self.score += 1
            return {
                "correct": True,
                "message": "✅ Correct! Well done.",
                "explanation": q["explanation"],
            }
        else:
            return {
                "correct": False,
                "message": f"❌ Incorrect! Correct answer was {q['answer']}.",
                "explanation": q["explanation"],
            }

    def play_interactive(self):
        """Play the quiz interactively."""
        print("\n" + "=" * 50)
        print("🧠 Welcome to the Software Development Trivia Quiz!")
        print(f"Answer {self.total_questions} questions. Each correct answer earns 1 point.")
        print("=" * 50)

        for i, q in enumerate(self.QUESTIONS):
            print(f"\nQuestion {i + 1} of {self.total_questions}:")
            print(q["question"])
            for opt in q["options"]:
                print(f"  {opt}")

            ans = ""
            while ans not in ("A", "B", "C", "D"):
                ans = input("Your answer (A, B, C, or D): ").strip().upper()
                if ans in ("Q", "QUIT", "EXIT"):
                    print("Quiz terminated early.")
                    return

            res = self.evaluate_answer(i, ans)
            print(res["message"])
            print(f"💡 Explanation: {res['explanation']}")

        percentage = (self.score / self.total_questions) * 100
        print("\n" + "=" * 50)
        print(f"📊 Quiz Complete! Your Score: {self.score}/{self.total_questions} ({percentage:.1f}%)")
        if percentage == 100:
            print("🏆 Outstanding! Perfect score, tech master!")
        elif percentage >= 60:
            print("👍 Great job! Solid software development knowledge.")
        else:
            print("📚 Good effort! Keep practicing and learning.")
        print("=" * 50)


def main():
    """Main entry point for Task 1."""
    while True:
        print("\n" + "=" * 50)
        print("   COGNIFYZ INTERNSHIP - TASK 1: TEXT-BASED GAME")
        print("=" * 50)
        print("1. Play Number Guessing Game")
        print("2. Play Software Development Trivia Quiz")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print("\nSelect Difficulty:")
            print("1. Easy (1 - 50, 10 attempts)")
            print("2. Medium (1 - 100, 7 attempts)")
            print("3. Hard (1 - 200, 5 attempts)")
            diff = input("Choose difficulty (1-3, default 2): ").strip() or "2"
            game = NumberGuessingGame(diff)
            game.play_interactive()
        elif choice == "2":
            quiz = TriviaQuizGame()
            quiz.play_interactive()
        elif choice == "3":
            print("Thank you for playing! Exiting Task 1.")
            break
        else:
            print("Invalid selection! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
