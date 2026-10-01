"""
Game logic engine for Rock, Paper, Scissors (and bonus Lizard, Spock expansion).
Includes move definitions, outcome calculators, AI strategies, and score/streak tracking.
"""

from enum import Enum
import random
from typing import Dict, List, Optional, Tuple


class Move(str, Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    LIZARD = "lizard"
    SPOCK = "spock"

    @classmethod
    def classic_moves(cls) -> List["Move"]:
        return [cls.ROCK, cls.PAPER, cls.SCISSORS]

    @classmethod
    def extended_moves(cls) -> List["Move"]:
        return [cls.ROCK, cls.PAPER, cls.SCISSORS, cls.LIZARD, cls.SPOCK]

    @classmethod
    def from_str(cls, value: str) -> Optional["Move"]:
        normalized = value.strip().lower()
        # Shorthand support
        shorthands = {
            "r": cls.ROCK,
            "p": cls.PAPER,
            "s": cls.SCISSORS,
            "l": cls.LIZARD,
            "k": cls.SPOCK,
            "sp": cls.SPOCK,
        }
        if normalized in shorthands:
            return shorthands[normalized]
        for move in cls:
            if move.value == normalized:
                return move
        return None


class Result(str, Enum):
    WIN = "win"
    LOSE = "lose"
    TIE = "tie"


# Define winning conditions and victory phrases
# WIN_RULES[move] = dict of {opponent_move: description}
WIN_RULES: Dict[Move, Dict[Move, str]] = {
    Move.ROCK: {
        Move.SCISSORS: "Rock crushes Scissors",
        Move.LIZARD: "Rock crushes Lizard",
    },
    Move.PAPER: {
        Move.ROCK: "Paper covers Rock",
        Move.SPOCK: "Paper disproves Spock",
    },
    Move.SCISSORS: {
        Move.PAPER: "Scissors cuts Paper",
        Move.LIZARD: "Scissors decapitates Lizard",
    },
    Move.LIZARD: {
        Move.SPOCK: "Lizard poisons Spock",
        Move.PAPER: "Lizard eats Paper",
    },
    Move.SPOCK: {
        Move.SCISSORS: "Spock smashes Scissors",
        Move.ROCK: "Spock vaporizes Rock",
    },
}

# ASCII Arts for each move
ASCII_ARTS: Dict[Move, str] = {
    Move.ROCK: r"""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
    Move.PAPER: r"""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
    Move.SCISSORS: r"""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
""",
    Move.LIZARD: r"""
      __
   .-'  )
  /  .-'
 (  (
  \  '-.
   '-.__) [Lizard]
""",
    Move.SPOCK: r"""
       __
      (  )
   .-'|  |'-.
  /   |  |   \
 (    |  |    ) [Spock]
  \          /
   '--------'
""",
}


def evaluate_round(player_move: Move, computer_move: Move) -> Tuple[Result, str]:
    """
    Evaluates the result of a single round from player's perspective.
    Returns (Result, explanation_string).
    """
    if player_move == computer_move:
        return Result.TIE, f"Both chose {player_move.value.capitalize()}! It's a draw."

    if computer_move in WIN_RULES[player_move]:
        phrase = WIN_RULES[player_move][computer_move]
        return Result.WIN, f"{phrase}! You win this round!"
    else:
        phrase = WIN_RULES[computer_move][player_move]
        return Result.LOSE, f"{phrase}! Computer wins this round!"


class AIStrategy:
    """Provides multiple AI decision-making engines."""

    @staticmethod
    def get_random_move(available_moves: List[Move]) -> Move:
        """Pure random choice."""
        return random.choice(available_moves)

    @staticmethod
    def get_smart_move(history: List[Tuple[Move, Move]], available_moves: List[Move]) -> Move:
        """
        Markov Chain / Pattern recognition predictor.
        Analyzes player's past sequence of choices to predict the next move and counter it.
        """
        if len(history) < 2:
            return AIStrategy.get_random_move(available_moves)

        # Transition matrix for player's move sequence
        transitions: Dict[Move, Dict[Move, int]] = {m: {m2: 0 for m2 in available_moves} for m in available_moves}
        player_moves = [h[0] for h in history]

        for i in range(len(player_moves) - 1):
            curr_move = player_moves[i]
            next_move = player_moves[i + 1]
            if curr_move in transitions and next_move in transitions[curr_move]:
                transitions[curr_move][next_move] += 1

        last_player_move = player_moves[-1]
        next_counts = transitions.get(last_player_move, {})
        most_likely_player_move = max(next_counts, key=next_counts.get) if any(next_counts.values()) else None

        if not most_likely_player_move:
            # Fallback to general frequency
            counts = {m: player_moves.count(m) for m in available_moves}
            most_likely_player_move = max(counts, key=counts.get)

        # Pick a move that beats predicted player move
        counters = [m for m in available_moves if most_likely_player_move in WIN_RULES[m]]
        return random.choice(counters) if counters else AIStrategy.get_random_move(available_moves)


class GameStats:
    """Keeps score, streaks, and round history."""

    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.current_streak = 0
        self.max_streak = 0
        self.history: List[Dict] = []

    def record_round(self, player_move: Move, computer_move: Move, result: Result, explanation: str):
        if result == Result.WIN:
            self.player_score += 1
            if self.current_streak >= 0:
                self.current_streak += 1
            else:
                self.current_streak = 1
            self.max_streak = max(self.max_streak, self.current_streak)
        elif result == Result.LOSE:
            self.computer_score += 1
            if self.current_streak <= 0:
                self.current_streak -= 1
            else:
                self.current_streak = -1
        else:
            self.ties += 1

        self.history.append({
            "round": len(self.history) + 1,
            "player": player_move.value,
            "computer": computer_move.value,
            "result": result.value,
            "explanation": explanation,
        })

    @property
    def total_rounds(self) -> int:
        return self.player_score + self.computer_score + self.ties

    @property
    def player_win_rate(self) -> float:
        if self.total_rounds == 0:
            return 0.0
        return (self.player_score / self.total_rounds) * 100

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.current_streak = 0
        self.max_streak = 0
        self.history.clear()
