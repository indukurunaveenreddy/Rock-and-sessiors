/**
 * Rock Paper Scissors Masters - Core Frontend Logic & Web Audio Synthesizer
 */

// Move configurations and Win rules
const MOVES = {
    rock: { emoji: '🪨', icon: '✊', beats: { scissors: 'crushes', lizard: 'crushes' } },
    paper: { emoji: '📄', icon: '✋', beats: { rock: 'covers', spock: 'disproves' } },
    scissors: { emoji: '✂️', icon: '✌️', beats: { paper: 'cuts', lizard: 'decapitates' } },
    lizard: { emoji: '🦎', icon: '🤏', beats: { spock: 'poisons', paper: 'eats' } },
    spock: { emoji: '🖖', icon: '🖖', beats: { scissors: 'smashes', rock: 'vaporizes' } },
};

// State
let mode = 'classic'; // 'classic' | 'extended'
let soundEnabled = true;
let isBattling = false;
let playerScore = 0;
let cpuScore = 0;
let tiesCount = 0;
let streak = 0;
let history = []; // array of { player, cpu, result, explanation }

// DOM Elements
const playerScoreEl = document.getElementById('player-score');
const cpuScoreEl = document.getElementById('cpu-score');
const tiesCountEl = document.getElementById('ties-count');
const streakCountEl = document.getElementById('streak-count');
const roundStatusEl = document.getElementById('round-status');
const roundExplanationEl = document.getElementById('round-explanation');
const playerHandIcon = document.getElementById('player-hand-icon');
const cpuHandIcon = document.getElementById('cpu-hand-icon');
const playerChoiceTag = document.getElementById('player-choice-tag');
const cpuChoiceTag = document.getElementById('cpu-choice-tag');
const historyLogEl = document.getElementById('history-log');
const soundToggleBtn = document.getElementById('sound-toggle');
const modeBtn = document.getElementById('theme-mode-btn');
const resetBtn = document.getElementById('reset-btn');
const aiSelect = document.getElementById('ai-select');
const extendedButtons = document.querySelectorAll('.extended-only');

// Web Audio API Synthesizer (Zero asset dependencies!)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, type = 'sine', duration = 0.1, gainVal = 0.15) {
    if (!soundEnabled || audioCtx.state === 'suspended') {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        if (!soundEnabled) return;
    }
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
        console.warn(e);
    }
}

function playWinSound() {
    playTone(523.25, 'triangle', 0.12); // C5
    setTimeout(() => playTone(659.25, 'triangle', 0.12), 100); // E5
    setTimeout(() => playTone(783.99, 'triangle', 0.25), 200); // G5
}

function playLoseSound() {
    playTone(400, 'sawtooth', 0.15, 0.1);
    setTimeout(() => playTone(280, 'sawtooth', 0.25, 0.1), 120);
}

function playTieSound() {
    playTone(350, 'sine', 0.15);
    setTimeout(() => playTone(350, 'sine', 0.15), 150);
}

function playClickSound() {
    playTone(600, 'sine', 0.05, 0.05);
}

// AI Engine (Markov Chain Predictor)
function getCpuMove() {
    const available = mode === 'classic' ? ['rock', 'paper', 'scissors'] : ['rock', 'paper', 'scissors', 'lizard', 'spock'];
    const aiType = aiSelect.value;

    if (aiType === 'casual' || history.length < 2) {
        return available[Math.floor(Math.random() * available.length)];
    }

    // Smart Markov prediction based on player transition history
    const transitions = {};
    available.forEach(m => transitions[m] = {});
    for (let i = 0; i < history.length - 1; i++) {
        const curr = history[i].player;
        const next = history[i + 1].player;
        if (transitions[curr]) {
            transitions[curr][next] = (transitions[curr][next] || 0) + 1;
        }
    }

    const lastMove = history[history.length - 1].player;
    const nextPossible = transitions[lastMove] || {};
    let predictedMove = null;
    let maxCount = -1;

    for (const [m, count] of Object.entries(nextPossible)) {
        if (count > maxCount) {
            maxCount = count;
            predictedMove = m;
        }
    }

    if (!predictedMove) {
        predictedMove = available[Math.floor(Math.random() * available.length)];
    }

    // Find move that beats the predicted move
    const winningCounters = available.filter(m => MOVES[m].beats && MOVES[m].beats[predictedMove]);
    return winningCounters.length > 0
        ? winningCounters[Math.floor(Math.random() * winningCounters.length)]
        : available[Math.floor(Math.random() * available.length)];
}

// Handle Battle
function executeBattle(playerMove) {
    if (isBattling) return;
    isBattling = true;
    playClickSound();

    // Reset hands to rock for countdown shaking
    playerHandIcon.textContent = '✊';
    cpuHandIcon.textContent = '✊';
    playerChoiceTag.textContent = 'Deciding...';
    cpuChoiceTag.textContent = 'Deciding...';
    roundStatusEl.textContent = 'Rock... Paper... Scissors...';
    roundStatusEl.className = 'round-status';
    roundExplanationEl.textContent = '';

    playerHandIcon.classList.add('anim-shake-left');
    cpuHandIcon.classList.add('anim-shake-right');

    // Shake sound ticks
    setTimeout(() => playTone(300, 'sine', 0.05), 0);
    setTimeout(() => playTone(300, 'sine', 0.05), 450);
    setTimeout(() => playTone(300, 'sine', 0.05), 900);

    setTimeout(() => {
        playerHandIcon.classList.remove('anim-shake-left');
        cpuHandIcon.classList.remove('anim-shake-right');

        const cpuMove = getCpuMove();

        // Reveal moves
        playerHandIcon.textContent = MOVES[playerMove].icon;
        cpuHandIcon.textContent = MOVES[cpuMove].icon;
        playerChoiceTag.textContent = capitalize(playerMove);
        cpuChoiceTag.textContent = capitalize(cpuMove);

        // Determine outcome
        let result = '';
        let explanation = '';

        if (playerMove === cpuMove) {
            result = 'tie';
            explanation = `Both selected ${capitalize(playerMove)}.`;
            tiesCount++;
            roundStatusEl.textContent = "It's a Draw! 🤝";
            roundStatusEl.className = 'round-status tie';
            playTieSound();
        } else if (MOVES[playerMove].beats && MOVES[playerMove].beats[cpuMove]) {
            result = 'win';
            const verb = MOVES[playerMove].beats[cpuMove];
            explanation = `${capitalize(playerMove)} ${verb} ${capitalize(cpuMove)}.`;
            playerScore++;
            streak = streak >= 0 ? streak + 1 : 1;
            roundStatusEl.textContent = "You Win! 🎉";
            roundStatusEl.className = 'round-status win';
            playWinSound();
            if (streak >= 3) triggerConfetti();
        } else {
            result = 'lose';
            const verb = MOVES[cpuMove].beats[playerMove];
            explanation = `${capitalize(cpuMove)} ${verb} ${capitalize(playerMove)}.`;
            cpuScore++;
            streak = streak <= 0 ? streak - 1 : -1;
            roundStatusEl.textContent = "Computer Wins! 💥";
            roundStatusEl.className = 'round-status lose';
            playLoseSound();
        }

        roundExplanationEl.textContent = explanation;

        // Record History
        history.push({ player: playerMove, cpu: cpuMove, result, explanation });
        updateUI();
        isBattling = false;
    }, 1400);
}

function updateUI() {
    playerScoreEl.textContent = playerScore;
    cpuScoreEl.textContent = cpuScore;
    tiesCountEl.textContent = tiesCount;
    streakCountEl.textContent = streak > 0 ? `+${streak}` : streak;

    // Update History Feed
    if (history.length === 0) {
        historyLogEl.innerHTML = '<div class="empty-history">No rounds played yet. Make a move above!</div>';
        return;
    }

    historyLogEl.innerHTML = history.slice(-6).reverse().map(item => `
        <div class="history-item ${item.result}">
            <span><strong>Round ${history.indexOf(item) + 1}</strong>: You (${MOVES[item.player].emoji}) vs CPU (${MOVES[item.cpu].emoji})</span>
            <span>${item.explanation}</span>
        </div>
    `).join('');
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Event Listeners
document.querySelectorAll('.weapon-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const move = btn.getAttribute('data-move');
        executeBattle(move);
    });
});

// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
    if (isBattling) return;
    const key = e.key.toLowerCase();
    if (key === 'r') executeBattle('rock');
    if (key === 'p') executeBattle('paper');
    if (key === 's') executeBattle('scissors');
    if (mode === 'extended') {
        if (key === 'l') executeBattle('lizard');
        if (key === 'k') executeBattle('spock');
    }
});

// Sound Toggle
soundToggleBtn.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    soundToggleBtn.textContent = soundEnabled ? '🔊' : '🔇';
    soundToggleBtn.title = soundEnabled ? 'Sound Enabled' : 'Sound Muted';
});

// Mode Toggle (Classic vs RPSLS)
modeBtn.addEventListener('click', () => {
    if (mode === 'classic') {
        mode = 'extended';
        modeBtn.textContent = 'Classic Mode';
        extendedButtons.forEach(b => b.classList.remove('hidden'));
    } else {
        mode = 'classic';
        modeBtn.textContent = 'RPSLS Mode';
        extendedButtons.forEach(b => b.classList.add('hidden'));
    }
});

// Reset Scores
resetBtn.addEventListener('click', () => {
    playerScore = 0;
    cpuScore = 0;
    tiesCount = 0;
    streak = 0;
    history = [];
    roundStatusEl.textContent = 'Scores reset! Pick your weapon to start.';
    roundStatusEl.className = 'round-status';
    roundExplanationEl.textContent = '';
    playerChoiceTag.textContent = 'Waiting...';
    cpuChoiceTag.textContent = 'Waiting...';
    playerHandIcon.textContent = '✊';
    cpuHandIcon.textContent = '✊';
    updateUI();
});

// Confetti Particle System
const canvas = document.getElementById('confetti-canvas');
const ctx = canvas.getContext('2d');
let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function triggerConfetti() {
    const colors = ['#38bdf8', '#10b981', '#f59e0b', '#ec4899', '#a855f7'];
    for (let i = 0; i < 80; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 2,
            vx: (Math.random() - 0.5) * 14,
            vy: (Math.random() - 0.7) * 14,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            alpha: 1,
            gravity: 0.25,
        });
    }
}

function updateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.alpha -= 0.015;
        if (p.alpha <= 0) {
            particles.splice(i, 1);
            continue;
        }
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(updateParticles);
}
requestAnimationFrame(updateParticles);
