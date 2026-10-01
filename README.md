# 🎮 Ultimate Rock Paper Scissors (Python & Web)

[![Python CI & Tests](https://github.com/your-username/rock-paper-scissors/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/rock-paper-scissors/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![Deploy to Pages](https://github.com/your-username/rock-paper-scissors/actions/workflows/pages.yml/badge.svg)](https://github.com/your-username/rock-paper-scissors/actions)

An advanced, feature-rich **Rock Paper Scissors** game developed in Python, featuring both an **interactive terminal CLI** with ASCII art and a **modern web UI** with Web Audio synthesizers, win streak counters, and an adaptive Markov Chain AI predictor.

Ready to deploy to **GitHub** and **GitHub Pages** with zero required external dependencies!

---

## ✨ Features

- 🕹️ **Dual Interfaces**:
  - **CLI Terminal Game** (`main.py`): ANSI colored interface with side-by-side ASCII art battles and countdowns.
  - **Modern Web App** (`web/` & `app.py`): Glassmorphic dark UI, 8-bit sound synthesizers, key bindings, and celebratory confetti particle effects.
- 🤖 **Smart AI Engine**:
  - **Casual Mode**: Standard randomizer.
  - **Smart Mode**: Markov-chain pattern recognition AI that analyzes your move sequences in real-time to predict your next throw.
- ⚔️ **Multiple Game Modes**:
  - **Classic**: Rock, Paper, Scissors.
  - **Extended (RPSLS)**: Rock, Paper, Scissors, Lizard, Spock (popularized by *The Big Bang Theory*).
- 🏆 **Formats & Match Tracking**:
  - Best of 3 (First to 2)
  - Best of 5 (First to 3)
  - Endless / Free play with win rate & streak records.
- 🧪 **100% Test Coverage**: Full suite of unit tests for all move combinations, tie outcomes, AI logic, and streak math.
- 🚀 **GitHub Ready**: Includes automated CI testing workflows and GitHub Pages auto-deploy actions.

---

## 📜 Game Rules

```
                      ┌───────────────┐
                      │    SCISSORS   │
                      └───────┬───────┘
                     /       │       \
             decapitates   cuts     crushes
                 /           │           \
                ▼            ▼            ▼
        ┌───────────┐      ┌───┐      ┌─────────┐
        │   LIZARD  │◄─eats┤ P │◄covers┤  ROCK   │
        └─────┬─────┘      │ A │      └────┬────┘
              │            │ P │           │
           poisons         │ E │        crushes
              │            │ R │           │
              ▼            └───┘           ▼
        ┌───────────┐                 ┌─────────┐
        │   SPOCK   │◄───disproves────┤  SPOCK  │
        └───────────┘                 └─────────┘
```

| Move | Beats | Reason |
| :--- | :--- | :--- |
| **🪨 Rock** | Scissors, Lizard | Rock crushes Scissors & crushes Lizard |
| **📄 Paper** | Rock, Spock | Paper covers Rock & disproves Spock |
| **✂️ Scissors** | Paper, Lizard | Scissors cuts Paper & decapitates Lizard |
| **🦎 Lizard** | Spock, Paper | Lizard poisons Spock & eats Paper |
| **🖖 Spock** | Scissors, Rock | Spock smashes Scissors & vaporizes Rock |

---

## 🚀 Quick Start

### 1. Run the Terminal CLI Game
No installations needed! Run directly with Python 3:

```bash
python3 main.py
```

### 2. Run the Web Interface Locally
Start the built-in web server:

```bash
python3 app.py
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

Keyboard shortcuts in web mode:
- `R` - Rock
- `P` - Paper
- `S` - Scissors
- `L` - Lizard (Extended mode)
- `K` - Spock (Extended mode)

---

## 🧪 Running Unit Tests

Run the automated test suite using Python's built-in `unittest` runner:

```bash
python3 -m unittest discover tests -v
```

---

## 📦 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml            # Automated CI tests for Python 3.9-3.13
│       └── pages.yml         # GitHub Pages automated deployment
├── tests/
│   └── test_game.py          # Comprehensive unit tests
├── web/
│   ├── index.html            # Web game HTML markup
│   ├── style.css             # Glassmorphism dark theme styles
│   └── app.js                # Web game logic, sound synths & confetti
├── app.py                    # Lightweight local web server launcher
├── game_logic.py             # Core game logic, rules engine & Markov AI
├── main.py                   # Terminal CLI interactive game
├── requirements.txt          # Optional dev dependencies
├── .gitignore                # Standard Python gitignore
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 🚢 Deploying to GitHub & GitHub Pages

### Step 1: Initialize Git and Commit
```bash
git init
git add .
git commit -m "feat: initial release of Ultimate Rock Paper Scissors"
```

### Step 2: Push to Your GitHub Repository
Create a new repository on [GitHub](https://github.com/new), then link and push:

```bash
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git
git push -u origin main
```

### Step 3: Enable Free GitHub Pages Web Hosting (Optional)
1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, select **GitHub Actions**.
4. Push any commit to `main`, and your game will be live at `https://<YOUR_USERNAME>.github.io/<YOUR_REPOSITORY_NAME>/`!

---

## 👨‍💻 Author

**Developed by Naveen Reddy**
- GitHub: [@your-username](https://github.com/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Copyright (c) 2026 Naveen Reddy.
