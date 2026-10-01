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


# ─── 🔥 MASS SONGS — Winner score >= 4 (dominant hype win) ──────────────────────
MASS_SONGS: List[Dict[str, str]] = [
    # ✅ User's mass/hype picks
    {"title": "Mass Song 1", "movie": "Telugu Mass Hit", "artist": "Mass Artist", "url": "https://youtu.be/JqFzhcWo3EU", "id": "JqFzhcWo3EU", "vibe": "mass"},
    {"title": "Mass Song 2", "movie": "Telugu Mass Hit", "artist": "Mass Artist", "url": "https://youtu.be/PCcpsw_tdIA", "id": "PCcpsw_tdIA", "vibe": "mass"},
    {"title": "Mass Song 3", "movie": "Telugu Mass Hit", "artist": "Mass Artist", "url": "https://youtu.be/9m3mT4KV3es", "id": "9m3mT4KV3es", "vibe": "mass"},
    # ✅ Mobcup songs (mass/hype)
    {"title": "Boom Boom Dude", "movie": "Telugu Mass Hit", "artist": "Mass Artist", "url": "https://mobcup.com.co/boom-boom-dude-telugu-song-ringtone-download-hiwefyq", "id": "JqFzhcWo3EU", "vibe": "mass"},
    {"title": "Trance of Omi", "movie": "Telugu Hit", "artist": "Thaman S", "url": "https://mobcup.com.co/trance-of-omi-thaman-s-telugu-song-ringtone-download-xa6r913", "id": "PCcpsw_tdIA", "vibe": "mass"},
    {"title": "Naa Praanama", "movie": "Telugu Folk", "artist": "Ram Miriyala", "url": "https://mobcup.com.co/naa-praanama-ram-miriyala-telugu-song-ringtone-download-mhq2po3", "id": "9m3mT4KV3es", "vibe": "mass"},
    {"title": "Rana Kumbha", "movie": "Telugu Hit", "artist": "Aditya Iyengar", "url": "https://mobcup.com.co/rana-kumbha-aditya-iyengar-telugu-song-ringtone-download-lf5ue9b", "id": "JqFzhcWo3EU", "vibe": "mass"},
    # Existing hype anthems
    {"title": "ButtaBomma", "movie": "Ala Vaikunthapurramuloo", "artist": "Armaan Malik, Thaman S", "url": "https://youtu.be/2mDCVzruYzQ", "id": "2mDCVzruYzQ", "vibe": "mass"},
    {"title": "Ramuloo Ramulaa", "movie": "Ala Vaikunthapurramuloo", "artist": "Anurag Kulkarni, Mangli, Thaman S", "url": "https://youtu.be/wFAj0pW6xX0", "id": "wFAj0pW6xX0", "vibe": "mass"},
    {"title": "Kurchi Madathapetti", "movie": "Guntur Kaaram", "artist": "Sahithi Chaganti, Sri Krishna, Thaman S", "url": "https://youtu.be/Ldn11dMHTJ8", "id": "Ldn11dMHTJ8", "vibe": "mass"},
    {"title": "Naatu Naatu", "movie": "RRR", "artist": "Rahul Sipligunj, Kaala Bhairava", "url": "https://www.youtube.com/watch?v=OsU0H507N0A", "id": "OsU0H507N0A", "vibe": "mass"},
    {"title": "Jinthaak", "movie": "Dhamaka", "artist": "Bheems Ceciroleo, Mangli", "url": "https://www.youtube.com/watch?v=QZ0D5Xv4XoQ", "id": "QZ0D5Xv4XoQ", "vibe": "mass"},
    {"title": "Ooru Palletooru", "movie": "Balagam / Folk", "artist": "Ram Miriyala, Mangli", "url": "https://www.youtube.com/watch?v=zR6z4Jq5bZQ", "id": "zR6z4Jq5bZQ", "vibe": "mass"},
    {"title": "Dhamaka Title Song", "movie": "Dhamaka", "artist": "Bheems Ceciroleo, Sahithi", "url": "https://www.youtube.com/watch?v=x2F4F7v5T1s", "id": "x2F4F7v5T1s", "vibe": "mass"},
    {"title": "Naatu Naatu", "movie": "RRR", "artist": "Rahul Sipligunj, Kaala Bhairava", "url": "https://www.youtube.com/watch?v=OsU0H507N0A", "id": "OsU0H507N0A", "vibe": "mass"},
    {"title": "Etthara Jenda", "movie": "RRR", "artist": "Vishal Dadlani, Prudhvi Chandra", "url": "https://www.youtube.com/watch?v=b4O4qV4Q-5I", "id": "b4O4qV4Q-5I", "vibe": "mass"},
    {"title": "Mind Block", "movie": "Sarileru Neekevvaru", "artist": "Blaaze, Ranina Reddy", "url": "https://www.youtube.com/watch?v=YwLh8E0t41g", "id": "YwLh8E0t41g", "vibe": "mass"},
    {"title": "Ranga Ranga Rangasthalana", "movie": "Rangasthalam", "artist": "Rahul Sipligunj", "url": "https://www.youtube.com/watch?v=LqN6_2O7tE8", "id": "LqN6_2O7tE8", "vibe": "mass"},
    {"title": "Jigelu Rani", "movie": "Rangasthalam", "artist": "Rela Kumar, Ganta Venkata Lakshmi", "url": "https://www.youtube.com/watch?v=VzN3_9H4hLo", "id": "VzN3_9H4hLo", "vibe": "mass"},
    {"title": "Komuram Bheemudo", "movie": "RRR", "artist": "Kaala Bhairava", "url": "https://www.youtube.com/watch?v=W3GqLp3FjUo", "id": "W3GqLp3FjUo", "vibe": "mass"},
    {"title": "Pulsar Bike", "movie": "Folk / Trending", "artist": "Jhansi, Ramana", "url": "https://www.youtube.com/watch?v=k9M7bM_N2X0", "id": "k9M7bM_N2X0", "vibe": "mass"},
    {"title": "Bullet (Bulletttu Bandi)", "movie": "Folk / Trending", "artist": "Mohana Bhogaraju", "url": "https://www.youtube.com/watch?v=P2Lshk3Q_yU", "id": "P2Lshk3Q_yU", "vibe": "mass"},
]

# ─── 😢 SAD SONGS — Winner score <= 3 (close / narrow / emotional result) ────────
SAD_SONGS: List[Dict[str, str]] = [
    # ✅ User's sad/emotional picks
    {"title": "Sad Song 1", "movie": "Telugu Emotional Hit", "artist": "Emotional Artist", "url": "https://youtu.be/6zDfwVSvyEk", "id": "6zDfwVSvyEk", "vibe": "sad"},
    {"title": "Sad Song 2", "movie": "Telugu Emotional Hit", "artist": "Emotional Artist", "url": "https://youtu.be/8PQNsHGhm2w", "id": "8PQNsHGhm2w", "vibe": "sad"},
    {"title": "Sad Song 3", "movie": "Telugu Emotional Hit", "artist": "Emotional Artist", "url": "https://youtu.be/Hx2kUN2kd1c", "id": "Hx2kUN2kd1c", "vibe": "sad"},
    # ✅ Mobcup songs (sad/emotional)
    {"title": "Ee Manase", "movie": "Tholiprema", "artist": "Deva", "url": "https://mobcup.com.co/ee-manase-tholiprema-telugu-ringtone-download-5pg2l06", "id": "6zDfwVSvyEk", "vibe": "sad"},
    {"title": "Ragile Ragile", "movie": "Telugu Hit", "artist": "Siddarth Basrur", "url": "https://mobcup.com.co/ragile-ragile-siddarth-basrur-telugu-song-ringtone-download-ms19h9i", "id": "8PQNsHGhm2w", "vibe": "sad"},
    {"title": "Padi Padi Leche Manasu BGM", "movie": "Padi Padi Leche Manasu", "artist": "Vishal Chandrasekhar", "url": "https://mobcup.com.co/padi-padi-leche-manasu-bgm-ringtones-download-naa-songs-9spfiao", "id": "Hx2kUN2kd1c", "vibe": "sad"},
    {"title": "Jabilamma Neeku Antha Kopama", "movie": "Telugu Folk", "artist": "Folk Artist", "url": "https://mobcup.com.co/jabilamma-neeku-antha-kopama-naa-songs-ringtone-download-173wv1z", "id": "6zDfwVSvyEk", "vibe": "sad"},
    {"title": "Kumkumala", "movie": "Brahmastra", "artist": "Pritam, Jonita Gandhi", "url": "https://mobcup.com.co/kumkumala-brahmastra-telugu-song-ringtone-download-k8odl91", "id": "8PQNsHGhm2w", "vibe": "sad"},
    # Existing emotional / soulful picks
    {"title": "Nee Kannu Neeli Samudram", "movie": "Uppena", "artist": "Javed Ali, Devi Sri Prasad", "url": "https://youtu.be/zZl7vDDN8Ek", "id": "zZl7vDDN8Ek", "vibe": "sad"},
    {"title": "Okey Oka Lokam", "movie": "Sashi", "artist": "Sid Sriram", "url": "https://www.youtube.com/watch?v=v0K8B4_L8r0", "id": "v0K8B4_L8r0", "vibe": "sad"},
    {"title": "Saranga Dariya", "movie": "Love Story", "artist": "Mangli", "url": "https://www.youtube.com/watch?v=d_2b2_2m678", "id": "d_2b2_2m678", "vibe": "sad"},
    {"title": "Chuttamalle", "movie": "Devara: Part 1", "artist": "Shilpa Rao, Anirudh Ravichander", "url": "https://www.youtube.com/watch?v=kXoYn7Y1Xb8", "id": "kXoYn7Y1Xb8", "vibe": "sad"},
    {"title": "Janani", "movie": "RRR", "artist": "MM Keeravaani", "url": "https://www.youtube.com/watch?v=e_0zN3_m3uY", "id": "e_0zN3_m3uY", "vibe": "sad"},
    {"title": "One Life", "movie": "Jersey", "artist": "Anirudh Ravichander", "url": "https://www.youtube.com/watch?v=4Y9eK1E5y4A", "id": "4Y9eK1E5y4A", "vibe": "sad"},
    {"title": "Nee Chitram Choosi", "movie": "Love Story", "artist": "Anurag Kulkarni", "url": "https://www.youtube.com/watch?v=QZ0P8i6a-E0", "id": "QZ0P8i6a-E0", "vibe": "sad"},
    {"title": "Ey Pilla", "movie": "Love Story", "artist": "Haricharan", "url": "https://www.youtube.com/watch?v=W0-h4R3F5jM", "id": "W0-h4R3F5jM", "vibe": "sad"},
    {"title": "Gira Gira", "movie": "Dear Comrade", "artist": "Gowtham Bharadwaj, Yamini Ghantasala", "url": "https://www.youtube.com/watch?v=X3x9pL7O1pM", "id": "X3x9pL7O1pM", "vibe": "sad"},
    {"title": "Dosti", "movie": "RRR", "artist": "Hemachandra, MM Keeravaani", "url": "https://www.youtube.com/watch?v=Gj9qU2sXF3E", "id": "Gj9qU2sXF3E", "vibe": "sad"},
    {"title": "Yentha Sakkagunnave", "movie": "Rangasthalam", "artist": "Devi Sri Prasad", "url": "https://www.youtube.com/watch?v=o8gJ-g6A_u4", "id": "o8gJ-g6A_u4", "vibe": "sad"},
    {"title": "Yesha Nagula Katta 🎵", "movie": "Telugu Folk Special", "artist": "Folk Sensation", "url": "https://www.youtube.com/watch?v=F0H1dO5wYc0", "id": "F0H1dO5wYc0", "vibe": "sad"},
]

# Combined pool (for backward compatibility / random pick)
TELUGU_WINNER_SONGS: List[Dict[str, str]] = MASS_SONGS + SAD_SONGS

# Backward compatibility alias
TOP_20_TELUGU_SONGS = TELUGU_WINNER_SONGS


def get_random_telugu_song() -> Dict[str, str]:
    """Selects a random song from the curated Telugu winner reward playlist."""
    return random.choice(TELUGU_WINNER_SONGS)


def get_song_by_score(winner_score: int) -> Dict[str, str]:
    """
    Selects a song based on the winner's score:
      - score >= 4  →  🔥 Mass/Hype song (dominant win)
      - score <= 3  →  😢 Sad/Emotional song (close/narrow result)
    """
    pool = MASS_SONGS if winner_score >= 4 else SAD_SONGS
    return random.choice(pool)
# Backward compatibility alias
TOP_20_TELUGU_SONGS = TELUGU_WINNER_SONGS


def get_random_telugu_song() -> Dict[str, str]:
    """Selects a random song from the curated Telugu winner reward playlist."""
    return random.choice(TELUGU_WINNER_SONGS)

