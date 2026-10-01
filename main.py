#!/usr/bin/env python3
"""
Rock Paper Scissors Tournament - Host & Multi-Player Edition
Developed by Naveen Reddy

Features:
- Host Management & Custom Player Names (Host can see all registered players)
- Modes: Player vs AI/Host OR 2-Player Local PvP
- 30-Second Original Telugu Superhit Victory Songs directly played via system audio!
"""

import getpass
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
    get_random_telugu_song,
    TELUGU_WINNER_SONGS,
)
from audio_player import play_winner_song_live, audio_controller

MAX_GAMES_LIMIT = 10


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
    BG_YELLOW = "\033[43m\033[30m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def host_dashboard_banner(host_name: str, p1_name: str, p2_name: str, match_mode: str):
    return f"""{Colors.CYAN}{Colors.BOLD}
=====================================================================
  👑  ROCK PAPER SCISSORS CHAMPIONSHIP - HOST DASHBOARD  👑
=====================================================================
  🎙️  HOST     : {Colors.YELLOW}{host_name}{Colors.CYAN}
  👥  PLAYERS  : {Colors.GREEN}{p1_name}{Colors.CYAN}  VS  {Colors.RED}{p2_name}{Colors.CYAN}
  🎯  MATCH    : {Colors.MAGENTA}{match_mode} (10 Games Tournament){Colors.CYAN}
====================================================================={Colors.RESET}"""


def print_side_by_side(art1: str, art2: str, label1: str, label2: str):
    lines1 = [line for line in art1.strip("\n").split("\n")]
    lines2 = [line for line in art2.strip("\n").split("\n")]
    max_height = max(len(lines1), len(lines2))
    width1 = max((len(l) for l in lines1), default=22)

    print(f"\n  {Colors.BOLD}{Colors.GREEN}{label1.center(width1)}{Colors.RESET}       VS       {Colors.BOLD}{Colors.RED}{label2}{Colors.RESET}")
    print("  " + "-" * (width1 + 32))
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


def setup_host_and_players() -> tuple:
    clear_screen()
    print(f"""{Colors.CYAN}{Colors.BOLD}
===========================================================
  🎮  ROCK PAPER SCISSORS - TOURNAMENT REGISTRATION  🎮
==========================================================={Colors.RESET}""")

    # 1. Host Setup
    host_input = input(f"\n{Colors.BOLD}{Colors.YELLOW}👑 Enter Tournament Host Name (default 'Naveen Reddy'):{Colors.RESET} ").strip()
    host_name = host_input if host_input else "Naveen Reddy"

    # 2. Match Mode Selection
    print(f"\n{Colors.BOLD}{Colors.WHITE}🎯 Select Match Type:{Colors.RESET}")
    print(f"  [{Colors.CYAN}1{Colors.RESET}] Single Player vs Host AI ({host_name})")
    print(f"  [{Colors.CYAN}2{Colors.RESET}] 2-Player Local PvP (Player 1 vs Player 2)")
    match_choice = ask_choice("Select [1/2] (default 1):", ["1", "2"], default="1")
    is_pvp = (match_choice == "2")

    # 3. Player Names
    p1_input = input(f"\n{Colors.BOLD}{Colors.GREEN}👤 Enter Player 1 Name (default 'Player 1'):{Colors.RESET} ").strip()
    p1_name = p1_input if p1_input else "Player 1"

    if is_pvp:
        p2_input = input(f"{Colors.BOLD}{Colors.RED}👤 Enter Player 2 Name (default 'Player 2'):{Colors.RESET} ").strip()
        p2_name = p2_input if p2_input else "Player 2"
    else:
        p2_name = host_name

    # 4. Weapons Mode
    print(f"\n{Colors.BOLD}{Colors.WHITE}⚔️ Select Game Weapons Mode:{Colors.RESET}")
    print(f"  [{Colors.CYAN}1{Colors.RESET}] Classic (Rock, Paper, Scissors)")
    print(f"  [{Colors.CYAN}2{Colors.RESET}] Extended (Rock, Paper, Scissors, Lizard, Spock)")
    mode_choice = ask_choice("Select mode [1/2] (default 1):", ["1", "2"], default="1")
    moves = Move.classic_moves() if mode_choice == "1" else Move.extended_moves()

    # 5. AI Strategy if not PvP
    smart_ai = True
    if not is_pvp:
        print(f"\n{Colors.BOLD}{Colors.WHITE}🤖 Choose {host_name}'s AI Strategy:{Colors.RESET}")
        print(f"  [{Colors.CYAN}1{Colors.RESET}] Casual (Random)")
        print(f"  [{Colors.CYAN}2{Colors.RESET}] Master (Markov Pattern Reader)")
        diff = ask_choice("Select strategy [1/2] (default 2):", ["1", "2"], default="2")
        smart_ai = (diff == "2")

    return host_name, p1_name, p2_name, is_pvp, moves, smart_ai


def play_game():
    host_name, p1_name, p2_name, is_pvp, moves, smart_ai = setup_host_and_players()
    stats = GameStats()
    raw_history = []
    total_rounds = MAX_GAMES_LIMIT

    match_mode_label = "2-Player PvP" if is_pvp else f"vs AI ({host_name})"

    try:
        for current_round in range(1, total_rounds + 1):
            clear_screen()
            print(host_dashboard_banner(host_name, p1_name, p2_name, match_mode_label))
            
            # Progress & Scoreboard
            progress_bar = "■" * (current_round - 1) + "□" * (total_rounds - current_round + 1)
            print(f"{Colors.BOLD}Match Score  : {Colors.GREEN}{p1_name} {stats.player_score}{Colors.RESET} - {Colors.RED}{p2_name} {stats.computer_score}{Colors.RESET} (Ties: {stats.ties})")
            print(f"{Colors.CYAN}Progress     : [{progress_bar}] ({current_round}/{total_rounds}){Colors.RESET}")
            if stats.current_streak > 1:
                print(f"{Colors.YELLOW}🔥 Win Streak : {stats.current_streak} | Max Streak: {stats.max_streak}{Colors.RESET}")

            print(f"\n{Colors.BOLD}--- Game {current_round} of {total_rounds} ---{Colors.RESET}")
            options_text = " / ".join([f"{m.value.capitalize()} ({m.value[0]})" for m in moves])
            print(f"Weapons: {Colors.CYAN}{options_text}{Colors.RESET} | Type 'q' to exit")

            # Player 1 Move
            while True:
                if is_pvp:
                    # In PvP, mask player 1 move so player 2 cannot peek
                    print(f"\n{Colors.GREEN}{p1_name}'s Turn (Secret input):{Colors.RESET}")
                    try:
                        p1_input = getpass.getpass(prompt=f"{p1_name}, enter move (e.g. r/p/s): ").strip()
                    except Exception:
                        p1_input = input(f"{p1_name}, enter move: ").strip()
                else:
                    p1_input = input(f"\n{Colors.GREEN}{p1_name}, enter your move:{Colors.RESET} ").strip()

                if p1_input.lower() in ["q", "quit", "exit"]:
                    print("\nTournament ended early by Host.")
                    return

                player_move = Move.from_str(p1_input)
                if player_move and player_move in moves:
                    break
                print(f"{Colors.RED}❌ Invalid move! Please choose from: {options_text}{Colors.RESET}")

            # Player 2 Move (AI or Human PvP)
            if is_pvp:
                while True:
                    print(f"\n{Colors.RED}{p2_name}'s Turn (Secret input):{Colors.RESET}")
                    try:
                        p2_input = getpass.getpass(prompt=f"{p2_name}, enter move (e.g. r/p/s): ").strip()
                    except Exception:
                        p2_input = input(f"{p2_name}, enter move: ").strip()

                    if p2_input.lower() in ["q", "quit", "exit"]:
                        print("\nTournament ended early by Host.")
                        return

                    opponent_move = Move.from_str(p2_input)
                    if opponent_move and opponent_move in moves:
                        break
                    print(f"{Colors.RED}❌ Invalid move! Please choose from: {options_text}{Colors.RESET}")
            else:
                if smart_ai:
                    opponent_move = AIStrategy.get_smart_move(raw_history, moves)
                else:
                    opponent_move = AIStrategy.get_random_move(moves)

            raw_history.append((player_move, opponent_move))

            # Countdown
            print(f"\n{Colors.CYAN}Rock...{Colors.RESET}", end="", flush=True)
            time.sleep(0.25)
            print(f" {Colors.CYAN}Paper...{Colors.RESET}", end="", flush=True)
            time.sleep(0.25)
            print(f" {Colors.CYAN}Scissors...{Colors.RESET}", end="", flush=True)
            time.sleep(0.25)
            print(f" {Colors.BOLD}{Colors.YELLOW}SHOOT!{Colors.RESET}\n")

            # Showdown
            print_side_by_side(
                ASCII_ARTS[player_move],
                ASCII_ARTS[opponent_move],
                f"{p1_name.upper()} ({player_move.value.upper()})",
                f"{p2_name.upper()} ({opponent_move.value.upper()})"
            )

            # Evaluate Round
            result, explanation = evaluate_round(player_move, opponent_move)
            # Format explanation with custom names
            custom_exp = explanation.replace("Computer", p2_name).replace("You", p1_name)
            stats.record_round(player_move, opponent_move, result, custom_exp)

            if result == Result.WIN:
                print(f"{Colors.BG_GREEN} 🎉 ROUND WIN! {Colors.RESET} {Colors.BOLD}{p1_name} wins! {custom_exp}{Colors.RESET}")
            elif result == Result.LOSE:
                print(f"{Colors.BG_RED} 💥 ROUND WIN! {Colors.RESET} {Colors.BOLD}{p2_name} wins! {custom_exp}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW} 🤝 TIE ROUND! {custom_exp}{Colors.RESET}")

            if current_round < total_rounds:
                input(f"\n{Colors.DIM}Host Press [Enter] for Game {current_round + 1}...{Colors.RESET}")

    except KeyboardInterrupt:
        print("\n\nTournament paused by Host.")

    # Tournament Completed - Winner Declaration
    clear_screen()
    print(host_dashboard_banner(host_name, p1_name, p2_name, match_mode_label))
    print(f"\n{Colors.CYAN}{Colors.BOLD}===========================================================")
    print(f"          🏆 10-GAMES TOURNAMENT FINAL STANDINGS 🏆")
    print(f"==========================================================={Colors.RESET}")
    print(f"Tournament Host       : {Colors.YELLOW}{host_name}{Colors.RESET}")
    print(f"Total Games Played    : {stats.total_rounds} / {MAX_GAMES_LIMIT}")
    print(f"{p1_name}'s Wins          : {Colors.GREEN}{stats.player_score}{Colors.RESET}")
    print(f"{p2_name}'s Wins          : {Colors.RED}{stats.computer_score}{Colors.RESET}")
    print(f"Ties / Draws          : {Colors.YELLOW}{stats.ties}{Colors.RESET}")
    print(f"{Colors.CYAN}==========================================================={Colors.RESET}\n")

    # Winner Declaration & 30-Second Original Song Playback
    song = get_random_telugu_song()

    if stats.player_score > stats.computer_score:
        winner = p1_name
        print(f"{Colors.BG_GREEN}{Colors.BOLD} 👑 CHAMPION: {winner.upper()} WON THE TOURNAMENT ({stats.player_score} - {stats.computer_score})! 👑 {Colors.RESET}\n")
    elif stats.computer_score > stats.player_score:
        winner = p2_name
        print(f"{Colors.BG_RED}{Colors.BOLD} 👑 CHAMPION: {winner.upper()} WON THE TOURNAMENT ({stats.computer_score} - {stats.player_score})! 👑 {Colors.RESET}\n")
    else:
        winner = f"{p1_name} & {p2_name}"
        print(f"{Colors.BG_YELLOW}{Colors.BOLD} 🤝 EPIC DRAW ({stats.player_score} - {stats.computer_score})! BOTH WARRIORS ARE WINNERS! 🤝 {Colors.RESET}\n")

    print(f"{Colors.BOLD}{Colors.YELLOW}🎙️ Host {host_name} dedicates the victory reward track to {winner}!{Colors.RESET}")
    play_winner_song_live(song, winner, host_name=host_name, duration=30)

    print(f"\n{Colors.CYAN}Tournament completed! Thank you for playing with Host {host_name}! ⭐{Colors.RESET}\n")


if __name__ == "__main__":
    play_game()
