/**
 * Rock Paper Scissors Masters - Host & Multi-Player Tournament Edition
 * Features:
 * - Tournament Host Management & Contestant Roster
 * - Single Player vs Host AI OR 2-Player Local PvP Mode
 * - 31 Curated Telugu Hit Songs & 30-Second Victory Celebration Engine
 */

// Move configurations and Win rules
const MOVES = {
    rock: { emoji: '🪨', icon: '✊', beats: { scissors: 'crushes', lizard: 'crushes' } },
    paper: { emoji: '📄', icon: '✋', beats: { rock: 'covers', spock: 'disproves' } },
    scissors: { emoji: '✂️', icon: '✌️', beats: { paper: 'cuts', lizard: 'decapitates' } },
    lizard: { emoji: '🦎', icon: '🤏', beats: { spock: 'poisons', paper: 'eats' } },
    spock: { emoji: '🖖', icon: '🖖', beats: { scissors: 'smashes', rock: 'vaporizes' } },
};

// 🔥 MASS SONGS — played when winner score >= 4 (dominant / hype win)
const MASS_SONGS = [
    // ✅ User's mass/hype picks (YouTube embed IDs)
    { title: "Mass Song 1",            movie: "Telugu Mass Hit",          artist: "Mass Artist",                    id: "JqFzhcWo3EU", vibe: "mass" },
    { title: "Mass Song 2",            movie: "Telugu Mass Hit",          artist: "Mass Artist",                    id: "PCcpsw_tdIA", vibe: "mass" },
    { title: "Mass Song 3",            movie: "Telugu Mass Hit",          artist: "Mass Artist",                    id: "9m3mT4KV3es", vibe: "mass" },
    // ✅ Mobcup songs (via YouTube) — mass/hype
    { title: "Boom Boom Dude",         movie: "Telugu Mass Hit",          artist: "Mass Artist",                    id: "JqFzhcWo3EU", vibe: "mass" },
    { title: "Trance of Omi",          movie: "Telugu Hit",               artist: "Thaman S",                      id: "PCcpsw_tdIA", vibe: "mass" },
    { title: "Naa Praanama",           movie: "Telugu Folk",              artist: "Ram Miriyala",                  id: "9m3mT4KV3es", vibe: "mass" },
    { title: "Rana Kumbha",            movie: "Telugu Hit",               artist: "Aditya Iyengar",                id: "JqFzhcWo3EU", vibe: "mass" },
    // Existing hype anthems
    { title: "ButtaBomma",             movie: "Ala Vaikunthapurramuloo",  artist: "Armaan Malik, Thaman S",         id: "2mDCVzruYzQ", vibe: "mass" },
    { title: "Ramuloo Ramulaa",        movie: "Ala Vaikunthapurramuloo",  artist: "Anurag Kulkarni, Mangli",        id: "wFAj0pW6xX0", vibe: "mass" },
    { title: "Kurchi Madathapetti",    movie: "Guntur Kaaram",            artist: "Sahithi Chaganti, Thaman S",     id: "Ldn11dMHTJ8", vibe: "mass" },
    { title: "Naatu Naatu",            movie: "RRR",                      artist: "Rahul Sipligunj, Kaala Bhairava",id: "2mDCVzruYzQ", vibe: "mass" },
    { title: "Jinthaak",              movie: "Dhamaka",                  artist: "Bheems Ceciroleo, Mangli",       id: "Ldn11dMHTJ8", vibe: "mass" },
    { title: "Ooru Palletooru",        movie: "Balagam",                  artist: "Ram Miriyala, Mangli",          id: "wFAj0pW6xX0", vibe: "mass" },
    // ✅ New user-added songs (Oct 2026)
    { title: "New Song 1",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "b6tvp-yyhYo", vibe: "mass" },
    { title: "New Song 2",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "g6VHdEJZhrY", vibe: "mass" },
    { title: "New Song 3",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "nBr5CQYotMU", vibe: "mass" },
    { title: "New Song 4",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "GzwccbaIsiw", vibe: "mass" },
    { title: "New Song 5",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "dI8JIDPFw0I", vibe: "mass" },
    { title: "New Song 6",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "qkFoz4kBE-Q", vibe: "mass" },
    { title: "New Song 7",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "h7xTXcRp4-4", vibe: "mass" },
    { title: "New Song 8",             movie: "Telugu Hit",               artist: "Telugu Artist",                  id: "UUvBougALf8", vibe: "mass" },
];

// 😢 SAD SONGS — played when winner score <= 3 (close/narrow win or low score)
const SAD_SONGS = [
    // ✅ User's sad/emotional picks
    { title: "Sad Song 1",             movie: "Telugu Emotional Hit",     artist: "Emotional Artist",               id: "6zDfwVSvyEk", vibe: "sad" },
    { title: "Sad Song 2",             movie: "Telugu Emotional Hit",     artist: "Emotional Artist",               id: "8PQNsHGhm2w", vibe: "sad" },
    { title: "Sad Song 3",             movie: "Telugu Emotional Hit",     artist: "Emotional Artist",               id: "Hx2kUN2kd1c", vibe: "sad" },
    // ✅ Mobcup songs (via YouTube) — sad/emotional
    { title: "Ee Manase",              movie: "Tholiprema",               artist: "Deva",                          id: "6zDfwVSvyEk", vibe: "sad" },
    { title: "Ragile Ragile",          movie: "Telugu Hit",               artist: "Siddarth Basrur",               id: "8PQNsHGhm2w", vibe: "sad" },
    { title: "Padi Padi Leche Manasu BGM", movie: "Padi Padi Leche Manasu", artist: "Vishal Chandrasekhar",        id: "Hx2kUN2kd1c", vibe: "sad" },
    { title: "Jabilamma Neeku Antha Kopama", movie: "Telugu Folk",        artist: "Folk Artist",                   id: "6zDfwVSvyEk", vibe: "sad" },
    { title: "Kumkumala",              movie: "Brahmastra",               artist: "Pritam, Jonita Gandhi",         id: "8PQNsHGhm2w", vibe: "sad" },
    // Existing emotional/soulful songs
    { title: "Nee Kannu Neeli Samudram",movie: "Uppena",                  artist: "Javed Ali, Devi Sri Prasad",     id: "zZl7vDDN8Ek", vibe: "sad" },
    { title: "Okey Oka Lokam",         movie: "Sashi",                    artist: "Sid Sriram",                    id: "zZl7vDDN8Ek", vibe: "sad" },
    { title: "Saranga Dariya",         movie: "Love Story",               artist: "Mangli",                        id: "Hx2kUN2kd1c", vibe: "sad" },
    { title: "Chuttamalle",            movie: "Devara: Part 1",           artist: "Shilpa Rao, Anirudh",           id: "8PQNsHGhm2w", vibe: "sad" },
];

// Combined pool (for shuffle button — plays any song)
const TELUGU_WINNER_SONGS = [...MASS_SONGS, ...SAD_SONGS];

// Helper — pick a random song from a given pool
function pickSong(pool) {
    return pool[Math.floor(Math.random() * pool.length)];
}

// Select song vibe based on winner's score
// score >= 4 → MASS (dominant win) | score <= 3 → SAD (close / narrow)
function pickSongByScore(winnerScore) {
    if (winnerScore >= 4) {
        return pickSong(MASS_SONGS);
    } else {
        return pickSong(SAD_SONGS);
    }
}

const MAX_GAMES = 10;

// Tournament Host & Player State
let hostName = "Naveen Reddy";
let player1Name = "Player 1";
let player2Name = "Naveen Reddy";
let matchMode = "ai"; // "ai" or "pvp"
let pvpPendingP1Move = null;

let rosterList = [
    { name: "Naveen Reddy", role: "Host / Master AI", wins: 0, losses: 0, status: "Active" },
    { name: "Player 1", role: "Contestant", wins: 0, losses: 0, status: "Active" },
    { name: "Player 2", role: "Contestant", wins: 0, losses: 0, status: "Standby" },
];

// Match State
let mode = 'classic';
let soundEnabled = true;
let isBattling = false;
let tournamentOver = false;
let currentGame = 1;
let playerScore = 0;
let cpuScore = 0;
let tiesCount = 0;
let streak = 0;
let history = [];
let rewardTimerInterval = null;
let activeWinnerName = "Player 1";

// DOM Elements
const hostNameDisplay = document.getElementById('host-name-display');
const p1HeaderTag = document.getElementById('p1-header-tag');
const p2HeaderTag = document.getElementById('p2-header-tag');
const matchTypePill = document.getElementById('match-type-pill');
const hostManagerBtn = document.getElementById('host-manager-btn');
const hostModal = document.getElementById('host-modal');
const hostModalClose = document.getElementById('host-modal-close');
const hostForm = document.getElementById('host-form');
const inputHostName = document.getElementById('input-host-name');
const inputP1Name = document.getElementById('input-p1-name');
const inputP2Name = document.getElementById('input-p2-name');
const p2Label = document.getElementById('p2-label');
const labelModeAi = document.getElementById('label-mode-ai');
const labelModePvp = document.getElementById('label-mode-pvp');
const rosterTbody = document.getElementById('roster-tbody');
const btnAddRosterPlayer = document.getElementById('btn-add-roster-player');

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
const gameProgressText = document.getElementById('game-progress-text');
const progressFill = document.getElementById('progress-fill');

// Modal Elements
const victoryModal = document.getElementById('victory-modal');
const modalTrophy = document.getElementById('modal-trophy');
const modalTitle = document.getElementById('modal-title');
const modalSubtitle = document.getElementById('modal-subtitle');
const modalScore = document.getElementById('modal-score');
const winnerDedicationTag = document.getElementById('winner-dedication-tag');
const songTitleEl = document.getElementById('song-title');
const songDetailsEl = document.getElementById('song-details');
const rewardTimerText = document.getElementById('reward-timer-text');
const rewardTimerBar = document.getElementById('reward-timer-bar');
const audioWaves = document.getElementById('audio-waves');
const btnShuffleSong = document.getElementById('btn-shuffle-song');
const btnAudioToggle = document.getElementById('btn-audio-toggle');
const audioStatusText = document.getElementById('audio-status-text');
const visualizerCanvas = document.getElementById('audio-visualizer');
const modalRestartBtn = document.getElementById('btn-modal-restart');

// Web Audio API (for UI sounds only — win/lose/tie tones)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let visualizerAnimFrame = null;
let isRewardPlaying = false;
let rewardIframe = null;   // holds the live YouTube embed iframe
let waveAnimInterval = null;

// ─── YouTube Embed Player ────────────────────────────────────────────────────
// Builds an autoplay embed URL. YouTube requires autoplay=1 + mute=0.
// The song plays in-page inside an invisible iframe — no redirect to YouTube.
function buildEmbedUrl(videoId) {
    return `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&mute=0&controls=1&rel=0&modestbranding=1&fs=0`;
}

function injectSongIframe(song) {
    // Remove previous iframe if any
    const existing = document.getElementById('song-embed-iframe');
    if (existing) existing.remove();

    const iframe = document.createElement('iframe');
    iframe.id = 'song-embed-iframe';
    iframe.width = '100%';
    iframe.height = '80';
    iframe.style.cssText = 'border:none;border-radius:12px;display:block;margin-top:8px;';
    iframe.allow = 'autoplay; encrypted-media';
    iframe.allowFullscreen = false;
    iframe.src = buildEmbedUrl(song.id);
    rewardIframe = iframe;

    const container = document.getElementById('song-iframe-container');
    if (container) container.appendChild(iframe);
}

function removeSongIframe() {
    const iframe = document.getElementById('song-embed-iframe');
    if (iframe) {
        // Mute by replacing src, then remove
        iframe.src = '';
        iframe.remove();
    }
    rewardIframe = null;
}

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
    playTone(523.25, 'triangle', 0.12);
    setTimeout(() => playTone(659.25, 'triangle', 0.15), 100);
    setTimeout(() => playTone(783.99, 'triangle', 0.25), 200);
}

function playLoseSound() {
    playTone(392.00, 'sawtooth', 0.15);
    setTimeout(() => playTone(329.63, 'sawtooth', 0.15), 120);
    setTimeout(() => playTone(261.63, 'sawtooth', 0.3), 240);
}

function playTieSound() {
    playTone(440, 'sine', 0.1);
    setTimeout(() => playTone(440, 'sine', 0.2), 150);
}

function playChampionshipFanfare() {
    if (!soundEnabled) return;
    const notes = [523.25, 659.25, 783.99, 1046.50, 783.99, 1046.50];
    notes.forEach((freq, idx) => {
        setTimeout(() => playTone(freq, 'triangle', 0.25, 0.2), idx * 180);
    });
}

// ─── CSS Wave bar animation helper (CSS-driven, no Web Audio needed for visuals) ─
function startWaveAnim() {
    if (audioWaves) audioWaves.classList.remove('paused');
}
function stopWaveAnim() {
    if (audioWaves) audioWaves.classList.add('paused');
}

// ─── Fake class to keep existing stop() call site happy ───────────────────────
class TeluguMusicSynthesizer {
    constructor() {}
    start() {}
    stop() { removeSongIframe(); stopWaveAnim(); }
}

// (Old synthesizer class removed — YouTube embed handles real audio)

// Canvas Equalizer Animation (CSS-wave based — no Web Audio analyser needed)
function startVisualizer() {
    startWaveAnim();
    if (!visualizerCanvas) return;
    // Animate canvas with random bars to simulate EQ visualizer
    const vCtx = visualizerCanvas.getContext('2d');
    function draw() {
        visualizerAnimFrame = requestAnimationFrame(draw);
        vCtx.fillStyle = 'rgba(15, 23, 42, 0.4)';
        vCtx.fillRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
        const bars = 32;
        const barWidth = visualizerCanvas.width / bars - 2;
        for (let i = 0; i < bars; i++) {
            const barHeight = (Math.random() * 0.7 + 0.1) * visualizerCanvas.height;
            const r = 56 + i * 4;
            const g = 189 - i * 3;
            vCtx.fillStyle = `rgb(${r},${g},248)`;
            vCtx.fillRect(i * (barWidth + 2), visualizerCanvas.height - barHeight, barWidth, barHeight);
        }
    }
    draw();
}

function stopVisualizer() {
    if (visualizerAnimFrame) {
        cancelAnimationFrame(visualizerAnimFrame);
        visualizerAnimFrame = null;
    }
}

// AI Move Selector
function getCpuMove() {
    const availableMoves = mode === 'classic'
        ? ['rock', 'paper', 'scissors']
        : ['rock', 'paper', 'scissors', 'lizard', 'spock'];

    if (aiSelect.value === 'casual' || history.length < 2) {
        return availableMoves[Math.floor(Math.random() * availableMoves.length)];
    }

    // Markov Prediction
    const lastPlayerMove = history[history.length - 1].player;
    const transitions = {};

    for (let i = 0; i < history.length - 1; i++) {
        if (history[i].player === lastPlayerMove) {
            const nextMove = history[i + 1].player;
            transitions[nextMove] = (transitions[nextMove] || 0) + 1;
        }
    }

    let predictedMove = null;
    let maxFreq = 0;
    for (const m in transitions) {
        if (transitions[m] > maxFreq && availableMoves.includes(m)) {
            maxFreq = transitions[m];
            predictedMove = m;
        }
    }

    if (!predictedMove) {
        predictedMove = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    }

    const counters = availableMoves.filter(m => MOVES[m].beats && MOVES[m].beats[predictedMove]);
    return counters.length > 0
        ? counters[Math.floor(Math.random() * counters.length)]
        : availableMoves[Math.floor(Math.random() * availableMoves.length)];
}

// Update Roster Table View
function renderRoster() {
    if (!rosterTbody) return;
    rosterTbody.innerHTML = rosterList.map((player, idx) => `
        <tr>
            <td><strong>${player.name}</strong></td>
            <td><span class="badge-role">${player.role}</span></td>
            <td style="color: #10b981;">${player.wins}</td>
            <td style="color: #ef4444;">${player.losses}</td>
            <td><span class="status-active">${player.status}</span></td>
        </tr>
    `).join('');
}

// Execute Battle
function executeBattle(moveChoice) {
    if (isBattling || tournamentOver) return;

    if (matchMode === "pvp") {
        if (!pvpPendingP1Move) {
            // Player 1 selected move, now wait for Player 2
            pvpPendingP1Move = moveChoice;
            roundStatusEl.textContent = `🔒 ${player1Name} selected move! Now ${player2Name}, pick your move!`;
            roundStatusEl.className = 'round-status tie';
            playerChoiceTag.textContent = 'Move Locked 🔒';
            return;
        }
    }

    isBattling = true;
    const p1Move = matchMode === "pvp" ? pvpPendingP1Move : moveChoice;
    const p2Move = matchMode === "pvp" ? moveChoice : getCpuMove();
    pvpPendingP1Move = null;

    playerHandIcon.textContent = '✊';
    cpuHandIcon.textContent = '✊';
    playerChoiceTag.textContent = 'Ready...';
    cpuChoiceTag.textContent = 'Ready...';
    roundStatusEl.textContent = 'Rock... Paper... Scissors...';
    roundStatusEl.className = 'round-status';
    roundExplanationEl.textContent = '';

    playerHandIcon.classList.add('anim-shake-left');
    cpuHandIcon.classList.add('anim-shake-right');

    setTimeout(() => playTone(300, 'sine', 0.05), 0);
    setTimeout(() => playTone(300, 'sine', 0.05), 450);
    setTimeout(() => playTone(300, 'sine', 0.05), 900);

    setTimeout(() => {
        playerHandIcon.classList.remove('anim-shake-left');
        cpuHandIcon.classList.remove('anim-shake-right');

        playerHandIcon.textContent = MOVES[p1Move].icon;
        cpuHandIcon.textContent = MOVES[p2Move].icon;
        playerChoiceTag.textContent = capitalize(p1Move);
        cpuChoiceTag.textContent = capitalize(p2Move);

        let result = '';
        let explanation = '';

        if (p1Move === p2Move) {
            result = 'tie';
            explanation = `Both selected ${capitalize(p1Move)}.`;
            tiesCount++;
            roundStatusEl.textContent = "It's a Draw! 🤝";
            roundStatusEl.className = 'round-status tie';
            playTieSound();
        } else if (MOVES[p1Move].beats && MOVES[p1Move].beats[p2Move]) {
            result = 'win';
            const verb = MOVES[p1Move].beats[p2Move];
            explanation = `${capitalize(p1Move)} ${verb} ${capitalize(p2Move)}.`;
            playerScore++;
            streak = streak >= 0 ? streak + 1 : 1;
            roundStatusEl.textContent = `${player1Name} Wins this game! 🎉`;
            roundStatusEl.className = 'round-status win';
            playWinSound();
        } else {
            result = 'lose';
            const verb = MOVES[p2Move].beats[p1Move];
            explanation = `${capitalize(p2Move)} ${verb} ${capitalize(p1Move)}.`;
            cpuScore++;
            streak = streak <= 0 ? streak - 1 : -1;
            roundStatusEl.textContent = `${player2Name} Wins this game! 💥`;
            roundStatusEl.className = 'round-status lose';
            playLoseSound();
        }

        roundExplanationEl.textContent = explanation;
        history.push({ player: p1Move, cpu: p2Move, result, explanation });

        currentGame++;
        if (currentGame > MAX_GAMES) {
            tournamentOver = true;
            finishTournament();
        }

        updateUI();
        isBattling = false;
    }, 1400);
}

// ─── Start 30-Second Reward Playback (Real Song via YouTube Embed) ───────────
function startRewardPlayback(song, winnerName) {
    // Clear existing timer
    if (rewardTimerInterval) clearInterval(rewardTimerInterval);

    // Remove any existing iframe (stops previous song)
    removeSongIframe();

    // Update song info UI
    if (songTitleEl) songTitleEl.textContent = song.title;
    if (songDetailsEl) songDetailsEl.textContent = `Movie: ${song.movie} • Singer: ${song.artist}`;
    if (winnerDedicationTag) winnerDedicationTag.textContent = `👑 Host ${hostName} dedicates this victory track to ${winnerName}! 👑`;
    if (audioStatusText) audioStatusText.textContent = `🎵 Now Playing: ${song.title}`;
    if (btnAudioToggle) btnAudioToggle.textContent = '⏸️ Pause';

    // Inject YouTube embed iframe — song plays in-page automatically
    injectSongIframe(song);
    isRewardPlaying = true;

    // Start CSS wave animation & canvas visualizer
    startVisualizer();

    // 30-second countdown timer
    let secondsLeft = 30;
    const totalSecs = 30;
    if (rewardTimerText) rewardTimerText.textContent = `${secondsLeft}s / ${totalSecs}s`;
    if (rewardTimerBar) rewardTimerBar.style.width = '100%';

    rewardTimerInterval = setInterval(() => {
        secondsLeft--;
        if (secondsLeft <= 0) {
            clearInterval(rewardTimerInterval);
            if (rewardTimerText) rewardTimerText.textContent = `00s / ${totalSecs}s ✅`;
            if (rewardTimerBar) rewardTimerBar.style.width = '0%';
            stopVisualizer();
            stopWaveAnim();
            removeSongIframe();
            isRewardPlaying = false;
            if (btnAudioToggle) btnAudioToggle.textContent = '🔀 Play Another';
            if (audioStatusText) audioStatusText.textContent = '✨ 30-Second Celebration Complete!';
        } else {
            if (rewardTimerText) rewardTimerText.textContent = `${secondsLeft < 10 ? '0' : ''}${secondsLeft}s / ${totalSecs}s`;
            if (rewardTimerBar) rewardTimerBar.style.width = `${(secondsLeft / totalSecs) * 100}%`;
        }
    }, 1000);
}

// 10-Games Finish Logic
function finishTournament() {
    playChampionshipFanfare();
    triggerConfetti();

    modalScore.textContent = `${player1Name.toUpperCase()} ${playerScore} - ${cpuScore} ${player2Name.toUpperCase()}`;

    if (playerScore > cpuScore) {
        activeWinnerName = player1Name;
        modalTrophy.textContent = '👑';
        modalTitle.textContent = `🏆 ${player1Name.toUpperCase()} WON THE CUP! 🏆`;
        modalSubtitle.textContent = `Congratulations! ${player1Name} won the 10-games championship match!`;
        updateRosterWinner(player1Name, player2Name);
    } else if (cpuScore > playerScore) {
        activeWinnerName = player2Name;
        modalTrophy.textContent = '👑';
        modalTitle.textContent = `🏆 ${player2Name.toUpperCase()} WON THE CUP! 🏆`;
        modalSubtitle.textContent = `Congratulations! ${player2Name} scored more wins and claimed the title!`;
        updateRosterWinner(player2Name, player1Name);
    } else {
        activeWinnerName = `${player1Name} & ${player2Name}`;
        modalTrophy.textContent = '🤝';
        modalTitle.textContent = "🏆 IT'S A CHAMPIONSHIP TIE! 🏆";
        modalSubtitle.textContent = `Both ${player1Name} and ${player2Name} tied with equal scores!`;
    }

    // 🎵 Pick song vibe based on winner's score
    const winnerScore = playerScore > cpuScore ? playerScore : cpuScore;
    const chosenSong = pickSongByScore(winnerScore);
    const vibeLabel = chosenSong.vibe === 'mass' ? '🔥 Mass Celebration' : '😢 Emotional Vibes';
    if (audioStatusText) audioStatusText.textContent = `${vibeLabel} — ${winnerScore} wins`;
    startRewardPlayback(chosenSong, activeWinnerName);

    setTimeout(() => {
        victoryModal.classList.remove('hidden');
    }, 800);
}

function updateRosterWinner(winner, loser) {
    const w = rosterList.find(p => p.name === winner);
    if (w) w.wins++;
    const l = rosterList.find(p => p.name === loser);
    if (l) l.losses++;
    renderRoster();
}

function updateUI() {
    // Header tags
    hostNameDisplay.textContent = hostName;
    p1HeaderTag.textContent = player1Name;
    p2HeaderTag.textContent = player2Name;
    matchTypePill.textContent = matchMode === "pvp" ? "2-Player PvP" : "Single Player";

    // Scoreboard inline name inputs (sync to state)
    const p1Input = document.getElementById('direct-p1-input');
    const p2Input = document.getElementById('direct-p2-input');
    if (p1Input && p1Input.value && p1Input.value !== player1Name) player1Name = p1Input.value;
    if (p2Input && p2Input.value && p2Input.value !== player2Name) player2Name = p2Input.value;

    playerScoreEl.textContent = playerScore;
    cpuScoreEl.textContent = cpuScore;
    tiesCountEl.textContent = tiesCount;
    streakCountEl.textContent = streak > 0 ? `+${streak}` : streak;

    // Progress Bar — clamp displayGame so it never shows "Game 11 of 10"
    const displayGame = Math.min(currentGame, MAX_GAMES);
    const progressPercent = Math.min(100, (displayGame / MAX_GAMES) * 100);
    progressFill.style.width = `${progressPercent}%`;
    gameProgressText.textContent = tournamentOver
        ? `Tournament Complete (${MAX_GAMES}/${MAX_GAMES})`
        : `Game ${displayGame} of ${MAX_GAMES}`;

    // History Log
    if (history.length === 0) {
        historyLogEl.innerHTML = `<div class="empty-history">Tournament started! First to finish 10 games wins the title.</div>`;
        return;
    }

    historyLogEl.innerHTML = history.slice(-6).reverse().map(item => `
        <div class="history-item ${item.result}">
            <span><strong>Game ${history.indexOf(item) + 1}</strong>: ${player1Name} (${MOVES[item.player].emoji}) vs ${player2Name} (${MOVES[item.cpu].emoji})</span>
            <span>${item.explanation}</span>
        </div>
    `).join('');
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function restartTournament() {
    // Stop any active reward timer
    if (rewardTimerInterval) {
        clearInterval(rewardTimerInterval);
        rewardTimerInterval = null;
    }
    // Stop and remove song iframe
    removeSongIframe();
    stopVisualizer();
    stopWaveAnim();
    isRewardPlaying = false;

    // Reset all game state
    playerScore = 0;
    cpuScore = 0;
    tiesCount = 0;
    streak = 0;
    currentGame = 1;
    tournamentOver = false;
    pvpPendingP1Move = null;
    history = [];
    isBattling = false;

    // Hide victory modal
    victoryModal.classList.add('hidden');

    // Reset status text
    roundStatusEl.textContent = matchMode === 'pvp'
        ? `${player1Name}, pick your move for Game 1! 🎮`
        : `Pick your move for Game 1! 🎮`;
    roundStatusEl.className = 'round-status';
    roundExplanationEl.textContent = '';
    playerChoiceTag.textContent = 'Waiting...';
    cpuChoiceTag.textContent = `${player2Name} Ready`;
    playerHandIcon.textContent = '✊';
    cpuHandIcon.textContent = '✊';

    // Reset audio status UI
    if (audioStatusText) audioStatusText.textContent = '🎮 New Tournament Started!';
    if (rewardTimerText) rewardTimerText.textContent = '';
    if (rewardTimerBar) rewardTimerBar.style.width = '0%';
    if (btnAudioToggle) btnAudioToggle.textContent = '⏸️ Pause';

    updateUI();
}

// Host Form Setup
if (hostManagerBtn) {
    hostManagerBtn.addEventListener('click', () => {
        inputHostName.value = hostName;
        inputP1Name.value = player1Name;
        inputP2Name.value = player2Name;
        renderRoster();
        hostModal.classList.remove('hidden');
    });
}

if (hostModalClose) {
    hostModalClose.addEventListener('click', () => {
        hostModal.classList.add('hidden');
    });
}

document.querySelectorAll('input[name="match-mode-radio"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (e.target.value === 'ai') {
            labelModeAi.classList.add('active');
            labelModePvp.classList.remove('active');
            p2Label.textContent = "🤖 Opponent / AI Name:";
            inputP2Name.value = inputHostName.value || "Naveen Reddy";
        } else {
            labelModePvp.classList.add('active');
            labelModeAi.classList.remove('active');
            p2Label.textContent = "👤 Player 2 Name:";
            if (inputP2Name.value === (inputHostName.value || "Naveen Reddy")) {
                inputP2Name.value = "Player 2";
            }
        }
    });
});

if (hostForm) {
    hostForm.addEventListener('submit', (e) => {
        e.preventDefault();
        hostName = inputHostName.value.trim() || "Naveen Reddy";
        player1Name = inputP1Name.value.trim() || "Player 1";
        player2Name = inputP2Name.value.trim() || "Player 2";
        matchMode = document.querySelector('input[name="match-mode-radio"]:checked').value;

        // Register in roster if not already present
        [hostName, player1Name, player2Name].forEach(name => {
            if (!rosterList.find(p => p.name === name)) {
                rosterList.push({ name, role: name === hostName ? "Host" : "Contestant", wins: 0, losses: 0, status: "Active" });
            }
        });

        hostModal.classList.add('hidden');
        restartTournament();
    });
}

if (btnAddRosterPlayer) {
    btnAddRosterPlayer.addEventListener('click', () => {
        const newName = prompt("Enter new Contestant / Player Name:");
        if (newName && newName.trim()) {
            const cleanName = newName.trim();
            if (!rosterList.find(p => p.name === cleanName)) {
                rosterList.push({ name: cleanName, role: "Contestant", wins: 0, losses: 0, status: "Standby" });
                renderRoster();
            }
        }
    });
}

// Event Listeners
document.querySelectorAll('.weapon-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const move = btn.getAttribute('data-move');
        executeBattle(move);
    });
});

window.addEventListener('keydown', (e) => {
    if (isBattling || tournamentOver) return;
    const key = e.key.toLowerCase();
    if (key === 'r') executeBattle('rock');
    if (key === 'p') executeBattle('paper');
    if (key === 's') executeBattle('scissors');
    if (mode === 'extended') {
        if (key === 'l') executeBattle('lizard');
        if (key === 'k') executeBattle('spock');
    }
});

soundToggleBtn.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    soundToggleBtn.textContent = soundEnabled ? '🔊' : '🔇';
    soundToggleBtn.title = soundEnabled ? 'Sound Enabled' : 'Sound Muted';
});

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

if (btnShuffleSong) {
    btnShuffleSong.addEventListener('click', () => {
        const nextSong = TELUGU_WINNER_SONGS[Math.floor(Math.random() * TELUGU_WINNER_SONGS.length)];
        startRewardPlayback(nextSong, activeWinnerName);
    });
}

if (btnAudioToggle) {
    btnAudioToggle.addEventListener('click', () => {
        // Toggle: if playing remove iframe (pauses song), if not playing re-inject
        if (isRewardPlaying) {
            removeSongIframe();
            isRewardPlaying = false;
            if (btnAudioToggle) btnAudioToggle.textContent = '▶️ Resume Song';
            if (audioWaves) audioWaves.classList.add('paused');
            if (audioStatusText) audioStatusText.textContent = '⏸️ Song Paused';
            stopVisualizer();
        } else {
            // Find current song from title text and re-inject
            const currentTitle = songTitleEl ? songTitleEl.textContent : '';
            const song = TELUGU_WINNER_SONGS.find(s => s.title === currentTitle)
                      || TELUGU_WINNER_SONGS[Math.floor(Math.random() * TELUGU_WINNER_SONGS.length)];
            injectSongIframe(song);
            isRewardPlaying = true;
            if (btnAudioToggle) btnAudioToggle.textContent = '⏸️ Pause Song';
            if (audioWaves) audioWaves.classList.remove('paused');
            if (audioStatusText) audioStatusText.textContent = `🎵 Playing: ${song.title}`;
            startVisualizer();
        }
    });
}

resetBtn.addEventListener('click', restartTournament);
modalRestartBtn.addEventListener('click', restartTournament);

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
    const colors = ['#38bdf8', '#10b981', '#f59e0b', '#ec4899', '#a855f7', '#fbbf24'];
    for (let i = 0; i < 120; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 2,
            vx: (Math.random() - 0.5) * 16,
            vy: (Math.random() - 0.7) * 16,
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
        p.alpha -= 0.012;
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

// ─── Player Name Entry Modal on Page Load ─────────────────────────────────────
const nameEntryModal = document.getElementById('name-entry-modal');
const nameEntryForm  = document.getElementById('name-entry-form');
const nameEntryInput = document.getElementById('name-entry-input');
const directP1Input  = document.getElementById('direct-p1-input');
const directP2Input  = document.getElementById('direct-p2-input');

if (nameEntryForm) {
    nameEntryForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const enteredName = nameEntryInput.value.trim();
        if (!enteredName) return;

        // Set Player 1 globally
        player1Name = enteredName;
        if (directP1Input) directP1Input.value = enteredName;

        // Update roster
        const rp1 = rosterList.find(p => p.name === 'Player 1');
        if (rp1) rp1.name = enteredName;
        else rosterList.push({ name: enteredName, role: 'Contestant', wins: 0, losses: 0, status: 'Active' });

        // Close name modal
        nameEntryModal.classList.add('hidden');

        // Update all UI
        renderRoster();
        updateUI();

        // Resume AudioContext (browsers require user gesture)
        if (audioCtx.state === 'suspended') audioCtx.resume();
    });
}

// Sync scoreboard inline name inputs → game state on blur/change
if (directP1Input) {
    directP1Input.addEventListener('change', () => {
        const n = directP1Input.value.trim();
        if (n) { player1Name = n; updateUI(); }
    });
}
if (directP2Input) {
    directP2Input.addEventListener('change', () => {
        const n = directP2Input.value.trim();
        if (n) { player2Name = n; updateUI(); }
    });
}

// Click outside host modal to close
if (hostModal) {
    hostModal.addEventListener('click', (e) => {
        if (e.target === hostModal) hostModal.classList.add('hidden');
    });
}

// Initial UI Setup (name modal is shown; game not started yet)
renderRoster();
updateUI();
