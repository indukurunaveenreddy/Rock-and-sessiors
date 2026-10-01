"""
Unit tests for Rock, Paper, Scissors game logic engine.
Run via: python3 -m unittest discover tests
"""

import unittest
from game_logic import (
    Move,
    Result,
    evaluate_round,
    AIStrategy,
    GameStats,
    WIN_RULES,
)


class TestMoveParsing(unittest.TestCase):
    def test_move_from_string(self):
        self.assertEqual(Move.from_str("rock"), Move.ROCK)
        self.assertEqual(Move.from_str("PAPER"), Move.PAPER)
        self.assertEqual(Move.from_str("  scissors  "), Move.SCISSORS)
        self.assertEqual(Move.from_str("lizard"), Move.LIZARD)
        self.assertEqual(Move.from_str("spock"), Move.SPOCK)

    def test_shorthands(self):
        self.assertEqual(Move.from_str("r"), Move.ROCK)
        self.assertEqual(Move.from_str("p"), Move.PAPER)
        self.assertEqual(Move.from_str("s"), Move.SCISSORS)
        self.assertEqual(Move.from_str("l"), Move.LIZARD)
        self.assertEqual(Move.from_str("k"), Move.SPOCK)
        self.assertEqual(Move.from_str("sp"), Move.SPOCK)

    def test_invalid_move(self):
        self.assertIsNone(Move.from_str("fire"))
        self.assertIsNone(Move.from_str(""))
        self.assertIsNone(Move.from_str("123"))


class TestRoundEvaluation(unittest.TestCase):
    def test_classic_wins(self):
        res, _ = evaluate_round(Move.ROCK, Move.SCISSORS)
        self.assertEqual(res, Result.WIN)

        res, _ = evaluate_round(Move.PAPER, Move.ROCK)
        self.assertEqual(res, Result.WIN)

        res, _ = evaluate_round(Move.SCISSORS, Move.PAPER)
        self.assertEqual(res, Result.WIN)

    def test_classic_losses(self):
        res, _ = evaluate_round(Move.SCISSORS, Move.ROCK)
        self.assertEqual(res, Result.LOSE)

        res, _ = evaluate_round(Move.ROCK, Move.PAPER)
        self.assertEqual(res, Result.LOSE)

        res, _ = evaluate_round(Move.PAPER, Move.SCISSORS)
        self.assertEqual(res, Result.LOSE)

    def test_extended_rules(self):
        # Rock beats Lizard
        res, _ = evaluate_round(Move.ROCK, Move.LIZARD)
        self.assertEqual(res, Result.WIN)

        # Lizard beats Spock
        res, _ = evaluate_round(Move.LIZARD, Move.SPOCK)
        self.assertEqual(res, Result.WIN)

        # Spock beats Scissors
        res, _ = evaluate_round(Move.SPOCK, Move.SCISSORS)
        self.assertEqual(res, Result.WIN)

        # Scissors decapitates Lizard
        res, _ = evaluate_round(Move.SCISSORS, Move.LIZARD)
        self.assertEqual(res, Result.WIN)

        # Lizard eats Paper
        res, _ = evaluate_round(Move.LIZARD, Move.PAPER)
        self.assertEqual(res, Result.WIN)

        # Paper disproves Spock
        res, _ = evaluate_round(Move.PAPER, Move.SPOCK)
        self.assertEqual(res, Result.WIN)

        # Spock vaporizes Rock
        res, _ = evaluate_round(Move.SPOCK, Move.ROCK)
        self.assertEqual(res, Result.WIN)

    def test_ties(self):
        for move in Move.extended_moves():
            res, exp = evaluate_round(move, move)
            self.assertEqual(res, Result.TIE)
            self.assertIn("draw", exp.lower())


class TestGameStats(unittest.TestCase):
    def setUp(self):
        self.stats = GameStats()

    def test_initial_state(self):
        self.assertEqual(self.stats.player_score, 0)
        self.assertEqual(self.stats.computer_score, 0)
        self.assertEqual(self.stats.ties, 0)
        self.assertEqual(self.stats.total_rounds, 0)
        self.assertEqual(self.stats.player_win_rate, 0.0)

    def test_record_win_and_streak(self):
        self.stats.record_round(Move.ROCK, Move.SCISSORS, Result.WIN, "Win 1")
        self.assertEqual(self.stats.player_score, 1)
        self.assertEqual(self.stats.current_streak, 1)
        self.assertEqual(self.stats.max_streak, 1)

        self.stats.record_round(Move.PAPER, Move.ROCK, Result.WIN, "Win 2")
        self.assertEqual(self.stats.player_score, 2)
        self.assertEqual(self.stats.current_streak, 2)
        self.assertEqual(self.stats.max_streak, 2)

        # Loss resets positive streak
        self.stats.record_round(Move.ROCK, Move.PAPER, Result.LOSE, "Lose 1")
        self.assertEqual(self.stats.computer_score, 1)
        self.assertEqual(self.stats.current_streak, -1)
        self.assertEqual(self.stats.max_streak, 2)

    def test_win_rate_calculation(self):
        self.stats.record_round(Move.ROCK, Move.SCISSORS, Result.WIN, "Win")
        self.stats.record_round(Move.ROCK, Move.PAPER, Result.LOSE, "Lose")
        self.assertEqual(self.stats.total_rounds, 2)
        self.assertEqual(self.stats.player_win_rate, 50.0)


class TestAIStrategy(unittest.TestCase):
    def test_random_ai_returns_valid_move(self):
        moves = Move.classic_moves()
        for _ in range(20):
            choice = AIStrategy.get_random_move(moves)
            self.assertIn(choice, moves)

    def test_smart_ai_prediction(self):
        moves = Move.classic_moves()
        # Repeating Rock pattern
        history = [(Move.ROCK, Move.SCISSORS) for _ in range(5)]
        choice = AIStrategy.get_smart_move(history, moves)
        # Smart AI should predict player throws Rock and counter with Paper
        self.assertEqual(choice, Move.PAPER)


if __name__ == "__main__":
    unittest.main()
