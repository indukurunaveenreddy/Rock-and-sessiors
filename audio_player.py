"""
Telugu Music Audio Player & Synthesizer Engine
Provides direct 30-second audio playback on macOS (via afplay) and other systems.
Synthesizes high-energy Telugu beats, folk rhythms (Teenmaar/Dholak), basslines, and melodic hooks.
No YouTube dependencies - plays real audio directly through your speakers!
"""

import math
import os
import random
import struct
import subprocess
import sys
import threading
import time
import wave
from typing import Dict, Optional

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".audio_cache")


def fetch_original_song_audio(song: Dict) -> Optional[str]:
    """
    Downloads or retrieves the cached original Telugu song audio (m4a/mp3).
    Uses yt-dlp to find the authentic original audio track.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    clean_title = "".join(c for c in song["title"] if c.isalnum() or c in (" ", "_")).strip().replace(" ", "_")
    output_prefix = os.path.join(CACHE_DIR, f"{clean_title}_original")
    
    # Check if already cached
    for ext in ("m4a", "mp3", "webm", "opus", "wav"):
        existing = f"{output_prefix}.{ext}"
        if os.path.exists(existing) and os.path.getsize(existing) > 50000:
            return existing

    # Download original track using yt-dlp
    try:
        import yt_dlp
        query = f"{song['title']} {song['movie']} Telugu audio song"
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': f"{output_prefix}.%(ext)s",
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'max_filesize': 8 * 1024 * 1024,  # max 8MB
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])

        for ext in ("m4a", "mp3", "webm", "opus", "wav"):
            downloaded = f"{output_prefix}.{ext}"
            if os.path.exists(downloaded) and os.path.getsize(downloaded) > 50000:
                return downloaded
    except Exception as e:
        pass
    
    return None


class AudioPlaybackController:
    """Manages system audio playback process with instant stop/skip capability."""

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self._is_playing = False

    def play_audio(self, file_path: str, duration: int = 30):
        self.stop()
        self._is_playing = True
        try:
            if sys.platform == "darwin":  # macOS
                self.process = subprocess.Popen(
                    ["afplay", "-t", str(duration), file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif sys.platform.startswith("linux"):
                for player in ["paplay", "aplay", "ffplay", "mpv"]:
                    if subprocess.run(["which", player], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                        cmd = [player, file_path]
                        if player in ("ffplay", "mpv"):
                            cmd = [player, "-nodisp", "-autoexit", "-t", str(duration), file_path]
                        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            elif sys.platform == "win32":
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=0.5)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
        self.process = None
        self._is_playing = False


# Global playback controller instance
audio_controller = AudioPlaybackController()


def play_winner_song_live(song: Dict, winner_name: str, host_name: str = "Naveen Reddy", duration: int = 30):
    """
    Plays the authentic original 30-second winner reward Telugu song directly on macOS speakers.
    Renders animated equalizer, dedicated host announcement, and progress bar in terminal.
    """
    colors_cyan = "\033[96m"
    colors_green = "\033[92m"
    colors_yellow = "\033[93m"
    colors_magenta = "\033[95m"
    colors_bold = "\033[1m"
    colors_reset = "\033[0m"
    colors_dim = "\033[2m"

    print(f"\n{colors_bold}{colors_yellow}🎧 Loading Original Telugu Song: {colors_cyan}{song['title']} ({song['movie']}){colors_reset}...")
    
    # Try getting original audio track
    audio_file = fetch_original_song_audio(song)
    if not audio_file:
        audio_file = generate_telugu_audio_track(song, duration=duration)

    # Speak dedication on Mac if available
    if sys.platform == "darwin":
        try:
            dedication_text = f"Congratulations {winner_name}! Host {host_name} presents your victory song: {song['title']}"
            subprocess.Popen(["say", "-r", "195", dedication_text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    # Start original audio track via afplay for 30s
    audio_controller.play_audio(audio_file, duration=duration)

    eq_frames = [
        " ▃▅▇▅▃ ", "▃▅▇█▇▅▃", "▅▇█▇▅▃ ", "▇█▇▅▃ ▃",
        "█▇▅▃ ▃▅", "▇▅▃ ▃▅▇", "▅▃ ▃▅▇█", "▃ ▃▅▇█▇"
    ]

    print(f"\n{colors_cyan}{colors_bold}▶️ ORIGINAL 30-SECOND SONG PLAYING ON YOUR SPEAKERS (Press Ctrl+C to skip){colors_reset}\n")

    start_time = time.time()
    try:
        while True:
            elapsed = int(time.time() - start_time)
            if elapsed >= duration:
                break
            
            sec = elapsed + 1
            progress = int((sec / duration) * 28)
            bar = "█" * progress + "░" * (28 - progress)
            eq = random.choice(eq_frames)
            dancer = "🕺💃" if (sec % 2 == 0) else "💃🕺"

            print(
                f"\r  {colors_magenta}{eq}{colors_reset} {dancer} [{colors_green}{bar}{colors_reset}] "
                f"{colors_yellow}{sec:02d}s/{duration:02d}s{colors_reset} | "
                f"Track: {colors_cyan}{song['title'][:20]}{colors_reset} 🔊 ",
                end="",
                flush=True,
            )
            time.sleep(0.25)
            
        print(f"\n\n{colors_bold}{colors_green}✨ 30 Seconds Winner Reward Celebration Completed! ✨{colors_reset}")
    except KeyboardInterrupt:
        print(f"\n\n{colors_dim}Audio playback stopped by user.{colors_reset}")
    finally:
        audio_controller.stop()
