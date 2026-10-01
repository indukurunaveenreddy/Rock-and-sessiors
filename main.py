#!/usr/bin/env python3
"""
Rock Paper Scissors (and Lizard Spock) - Python CLI Game
Developed by Naveen Reddy

Features:
- ANSI color styling & ASCII art hands
- Classic & Extended Game Modes
- Casual & Smart Pattern-Predictor AI
- Best-of-3, Best-of-5 & Endless Modes
- Win streaks, Stats Tracker & Round History
"""

import os
import sys
import time
from game_logic import (
    Move,
    Result,
    evaluate_round,
    AIStrategy,
    GameStats,
    ASCII_ARTS,
)


class Colors:
    """ANSI color escapes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BG_CYAN = "\033[46m\033[30m"
    BG_GREEN = "\033[42m\033[30m"
    BG_RED = "\033[41m\033[97m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    return f"""{Colors.CYAN}{Colors.BOLD}
===========================================================
  🎮  ULTIMATE ROCK PAPER SCISSORS (CLI EDITION)  🎮
             Developed by Naveen Reddy
==========================================================={Colors.RESET}"""


def print_side_by_side(art1: str, art2: str, label1="YOU", label2="COMPUTER"):
    lines1 = [line for line in art1.strip("\n").split("\n")]
    lines2 = [line for line in art2.strip("\n").split("\n")]
    max_height = max(len(lines1), len(lines2))
    width1 = max((len(l) for l in lines1), default=20)

    print(f"\n  {Colors.BOLD}{Colors.GREEN}{label1.center(width1)}{Colors.RESET}       VS       {Colors.BOLD}{Colors.RED}{label2}{Colors.RESET}")
    print("  " + "-" * (width1 + 30))
    for i in range(max_height):
        l1 = lines1[i] if i < len(lines1) else ""
        l2 = lines2[i] if i < len(lines2) else ""
        print(f"  {Colors.GREEN}{l1.ljust(width1)}{Colors.RESET}            {Colors.RED}{l2}{Colors.RESET}")
    print()


def ask_choice(prompt: str, valid_options: list, default: str = None) -> str:
    while True:
        choice = input(f"{Colors.YELLOW}{prompt}{Colors.RESET} ").strip().lower()
        if not choice and default:
            return default
        if choice in valid_options:
            return choice
        print(f"{Colors.RED}❌ Invalid option. Choose from: {', '.join(valid_options)}{Colors.RESET}")


def select_game_mode() -> tuple:
    print(f"\n{Colors.BOLD}{Colors.WHITE}🎯 Choose Game Mode:{Colors.RESET}")
    print(f"  [{Colors.CYAN}1{Colors.RESET}] Classic (Rock, Paper, Scissors)")
    print(f"  [{Colors.CYAN}2{Colors.RESET}] Extended (Rock, Paper, Scissors, Lizard, Spock)")
    choice = ask_choice("Select mode [1/2] (default 1):", ["1", "2"], default="1")
    moves = Move.classic_moves() if choice == "1" else Move.extended_moves()

    print(f"\n{Colors.BOLD}{Colors.WHITE}🤖 Choose AI Difficulty:{Colors.RESET}")
    print(f"  [{Colors.CYAN}1{Colors.RESET}] Casual (Random selections)")
    print(f"  [{Colors.CYAN}2{Colors.RESET}] Smart (Adaptive Markov AI that reads patterns)")
    diff_choice = ask_choice("Select difficulty [1/2] (default 1):", ["1", "2"], default="1")
    smart_ai = (diff_choice == "2")

    print(f"\n{Colors.BOLD}{Colors.WHITE}🏆 Choose Match Format:{Colors.RESET}")
    print(f"  [{Colors.CYAN}1{Colors.RESET}] Best of 3 (First to 2 wins)")
    print(f"  [{Colors.CYAN}2{Colors.RESET}] Best of 5 (First to 3 wins)")
    print(f"  [{Colors.CYAN}3{Colors.RESET}] Endless / Free Play")
    target_choice = ask_choice("Select format [1/2/3] (default 3):", ["1", "2", "3"], default="3")
    target_wins = 2 if target_choice == "1" else (3 if target_choice == "2" else 0)

    return moves, smart_ai, target_wins


def play_game():
    clear_screen()
    print(banner())
    moves, smart_ai, target_wins = select_game_mode()
    stats = GameStats()

    raw_history = []  # tuple list for AI
    round_num = 1

    try:
        while True:
            clear_screen()
            print(banner())
            # Header info
            mode_str = "Classic" if len(moves) == 3 else "Extended (RPSLS)"
            ai_str = "Smart (Predictive)" if smart_ai else "Casual (Random)"
            print(f"{Colors.DIM}Mode: {mode_str} | AI: {ai_str} | Target: {'First to ' + str(target_wins) if target_wins > 0 else 'Endless'}{Colors.RESET}")
            print(f"{Colors.BOLD}Score: {Colors.GREEN}Player {stats.player_score}{Colors.RESET} - {Colors.RED}Computer {stats.computer_score}{Colors.RESET} (Ties: {stats.ties}){Colors.RESET}")
            if stats.current_streak > 1:
                print(f"{Colors.YELLOW}🔥 Win Streak: {stats.current_streak} | Max Streak: {stats.max_streak}{Colors.RESET}")

            print(f"\n{Colors.BOLD}--- Round {round_num} ---{Colors.RESET}")
            options_text = " / ".join([f"{m.value.capitalize()} ({m.value[0]})" for m in moves])
            print(f"Options: {Colors.CYAN}{options_text}{Colors.RESET} or {Colors.DIM}'q' to quit{Colors.RESET}")

            user_input = input(f"\n{Colors.YELLOW}Enter your move:{Colors.RESET} ").strip()
            if user_input.lower() in ["q", "quit", "exit"]:
                break

            player_move = Move.from_str(user_input)
            if not player_move or player_move not in moves:
                print(f"{Colors.RED}❌ Invalid move! Please select one of the available choices.{Colors.RESET}")
                time.sleep(1.2)
                continue

            # Countdown effect
            print(f"\n{Colors.CYAN}Rock...{Colors.RESET}", end="", flush=True)
            time.sleep(0.3)
            print(f" {Colors.CYAN}Paper...{Colors.RESET}", end="", flush=True)
            time.sleep(0.3)
            print(f" {Colors.CYAN}Scissors...{Colors.RESET}", end="", flush=True)
            time.sleep(0.3)
            print(f" {Colors.BOLD}{Colors.YELLOW}SHOOT!{Colors.RESET}\n")

            # Computer decision
            if smart_ai:
                computer_move = AIStrategy.get_smart_move(raw_history, moves)
            else:
                computer_move = AIStrategy.get_random_move(moves)

            raw_history.append((player_move, computer_move))

            # Visual Showdown
            print_side_by_side(ASCII_ARTS[player_move], ASCII_ARTS[computer_move], f"YOU ({player_move.value.upper()})", f"CPU ({computer_move.value.upper()})")

            # Evaluate round
            result, explanation = evaluate_round(player_move, computer_move)
            stats.record_round(player_move, computer_move, result, explanation)

            if result == Result.WIN:
                print(f"{Colors.BG_GREEN} 🎉 ROUND WON! {Colors.RESET} {Colors.BOLD}{explanation}{Colors.RESET}")
            elif result == Result.LOSE:
                print(f"{Colors.BG_RED} 💥 ROUND LOST! {Colors.RESET} {Colors.BOLD}{explanation}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW} 🤝 TIE! {explanation}{Colors.RESET}")

            # Check if match ended in target win mode
            if target_wins > 0:
                if stats.player_score >= target_wins:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}🏆 CONGRATULATIONS! You won the match ({stats.player_score} - {stats.computer_score})! 🏆{Colors.RESET}\n")
                    break
                elif stats.computer_score >= target_wins:
                    print(f"\n{Colors.RED}{Colors.BOLD}💀 GAME OVER! Computer won the match ({stats.computer_score} - {stats.player_score}).{Colors.RESET}\n")
                    break

            round_num += 1
            input(f"\n{Colors.DIM}Press [Enter] to continue to next round...{Colors.RESET}")

    except KeyboardInterrupt:
        print("\n\nGame paused by user.")

    # Game over summary
    print(f"\n{Colors.CYAN}{Colors.BOLD}===========================================================")
    print("                    📊 FINAL GAME STATS")
    print(f"==========================================================={Colors.RESET}")
    print(f"Total Rounds Played : {stats.total_rounds}")
    print(f"Player Wins         : {Colors.GREEN}{stats.player_score}{Colors.RESET}")
    print(f"Computer Wins       : {Colors.RED}{stats.computer_score}{Colors.RESET}")
    print(f"Draws / Ties        : {Colors.YELLOW}{stats.ties}{Colors.RESET}")
    print(f"Player Win Rate     : {stats.player_win_rate:.1f}%")
    print(f"Max Win Streak      : {stats.max_streak}")
    print(f"{Colors.CYAN}==========================================================={Colors.RESET}")
    print(f"Developed by {Colors.BOLD}Naveen Reddy{Colors.RESET} • Star the project on GitHub ⭐\n")


if __name__ == "__main__":
    play_game()
