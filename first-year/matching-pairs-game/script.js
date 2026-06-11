// --------------------------------
// Constants and element references
// --------------------------------
const SUITS = ["club", "diamond", "heart", "spade"];
const BACK_SRC = "./images/back.jpg";

// references
const boardEl = document.getElementById("board");
const boardPlaceholderEl = document.getElementById("boardPlaceholder");
const sizeFieldset = document.getElementById("sizeFieldset");
const controlsEl = document.getElementById("controls");
const statsEl = document.getElementById("stats");
const shuffleBtn = document.getElementById("shuffleBtn");
const startBtn = document.getElementById("startBtn");
const clickCountEl = document.getElementById("clickCount");
const pairCountEl = document.getElementById("pairCount");
const clickMaxEl = document.getElementById("clickMax");
const pairMaxEl = document.getElementById("pairMax");
const timerCountEl = document.getElementById("timerCount");
const dialogEl = document.getElementById("gameOverDialog");
const dialogMsgEl = document.getElementById("gameOverMessage");
const playAgainBtn = document.getElementById("playAgainBtn");
const cursorFxLayer = document.getElementById("cursorFxLayer");
const toggleHighContrastEl = document.getElementById("toggleHighContrast");
const toggleLargeTextEl = document.getElementById("toggleLargeText");
const toggleReducedMotionEl = document.getElementById("toggleReducedMotion");
const toggleColorModeEl = document.getElementById("toggleColorMode");
const themeSelectEl = document.getElementById("themeSelect");

// --------------
// Game state
// --------------
const state = {
  rows: 0,
  cards: [],
  shuffled: false,
  started: false,
  clicks: 0,
  pairs: 0,
  totalPairs: 0,
  selected: [],
  locked: false,
  elapsedTime: 0,
};

let timerInterval = null;

// -----------------
//  Timer functions
// -----------------

// start the game timer
function startTimer() {
  state.elapsedTime = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    state.elapsedTime += 1;
    updateTimerDisplay();
  }, 1000);
}

// Stop and clear the timer
function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

// Update timer
function updateTimerDisplay() {
  timerCountEl.textContent = `${state.elapsedTime}s`;
}

// -----------------------------
// Card generation and shuffling
// -----------------------------

//Ordered board
function createOrderedCards(rows) {
  const cards = [];
  for (let rank = 1; rank <= rows; rank += 1) {
    for (const suit of SUITS) {
      cards.push({ suit, rank, faceUp: true, matched: false });
    }
  }
  return cards;
}

// Shuffle cards w/ fisher yates algorithm
function shuffleCards(cards) {
  for (let i = cards.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }
}

// ----------------------
// Card display utilities
// ----------------------

function cardFaceSrc(card) {
  return `./images/${card.suit}_${card.rank}.png`;
}

// -----------
// UI updates
// -----------

// Update the counter
function updateStats() {
  const maxAllowedClicks = state.cards.length * 2;
  clickCountEl.textContent = String(state.clicks);
  clickMaxEl.textContent = `/${maxAllowedClicks}`;
  pairCountEl.textContent = String(state.pairs);
  pairMaxEl.textContent = `/${state.totalPairs}`;
}

// Enable or disable setup controls
function setSetupControlsEnabled(enabled) {
  shuffleBtn.disabled = !enabled;
  startBtn.disabled = !enabled;
  const radios = sizeFieldset.querySelectorAll('input[name="boardSize"]');
  radios.forEach((radio) => {
    radio.disabled = !enabled;
  });
}

// Render the game board
function renderBoard() {
  boardEl.innerHTML = "";

  state.cards.forEach((card, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "card";
    button.dataset.index = String(index);

    const img = document.createElement("img");
    const showBack = state.started && !card.faceUp;
    img.src = showBack ? BACK_SRC : cardFaceSrc(card);
    button.appendChild(img);

    // Disable cards before game start
    if (!state.started || card.faceUp || card.matched) button.disabled = true;
    if (card.matched) button.classList.add("matched");

    boardEl.appendChild(button);
  });
}

// Apply card flip animation
function animateCardFlip(button) {
  if (!button) return;
  button.classList.add("card-flip");
  setTimeout(() => {
    button.classList.remove("card-flip");
  }, 180);
}

// ----------------------------
// Game flow functions
// ----------------------------

// Show the win / loss message.
function showGameOver(won) {
  state.locked = true;
  stopTimer();
  dialogMsgEl.textContent = won ? "Congratulations!" : "Game over! Try again!";
  if (typeof dialogEl.showModal === "function") dialogEl.showModal();
  else alert(dialogMsgEl.textContent);
}

// Check if the game has ended
function checkEndConditions() {
  if (!state.started) return;
  if (state.pairs === state.totalPairs) showGameOver(true);
  else if (state.clicks > state.cards.length * 2) showGameOver(false);
}

// Reset game state and UI
function selectBoardSize(rows) {
  state.rows = rows;
  state.cards = createOrderedCards(rows);
  state.shuffled = false;
  state.started = false;
  state.clicks = 0;
  state.pairs = 0;
  state.totalPairs = state.cards.length / 2;
  state.selected = [];
  state.locked = false;

  boardPlaceholderEl.hidden = true;
  controlsEl.hidden = false;
  statsEl.hidden = true;
  setSetupControlsEnabled(true);
  updateStats();
  renderBoard();
}

// Shuffle the cards
function handleShuffle() {
  if (!state.rows || state.started) return;
  shuffleCards(state.cards);
  state.shuffled = true;
  renderBoard();
}

// Flip all cards face down
function beginGameplay() {
  state.started = true;
  state.clicks = 0;
  state.pairs = 0;
  state.selected = [];
  state.locked = false;

  state.cards.forEach((card) => {
    card.faceUp = false;
  });

  statsEl.hidden = false;
  setSetupControlsEnabled(false);
  startBtn.textContent = "Quit";
  startBtn.disabled = false;
  updateStats();
  startTimer();
  renderBoard();
}

// Handle Start button
function handleStart() {
  if (!state.rows) return;
  if (!state.shuffled) {
    alert("Please shuffle the cards before starting the game.");
    return;
  }
  beginGameplay();
}

// Handle Quit button
function handleQuit() {
  state.rows = 0;
  state.cards = [];
  state.shuffled = false;
  state.started = false;
  state.clicks = 0;
  state.pairs = 0;
  state.totalPairs = 0;
  state.selected = [];
  state.locked = false;
  state.elapsedTime = 0;

  boardPlaceholderEl.hidden = false;
  controlsEl.hidden = true;
  statsEl.hidden = true;
  startBtn.textContent = "Start";
  boardEl.innerHTML = "";
  setSetupControlsEnabled(true);
  stopTimer();

  // Clear board size selection.
  const radios = sizeFieldset.querySelectorAll('input[name="boardSize"]');
  radios.forEach((radio) => {
    radio.checked = false;
  });

  updateStats();
  updateTimerDisplay();
}

// ----------------------------
// Card interaction functions
// ----------------------------

// Mark two cards as matched
function markPairMatched(indexA, indexB) {
  state.cards[indexA].matched = true;
  state.cards[indexB].matched = true;
  const btnA = boardEl.querySelector(`.card[data-index="${indexA}"]`);
  const btnB = boardEl.querySelector(`.card[data-index="${indexB}"]`);
  if (btnA) btnA.classList.add("matched");
  if (btnB) btnB.classList.add("matched");
}

// Flip a card face down
function flipDownCard(index) {
  state.cards[index].faceUp = false;
  const button = boardEl.querySelector(`.card[data-index="${index}"]`);
  if (!button) return;
  const img = button.querySelector("img");
  if (!img) return;
  animateCardFlip(button);
  img.src = BACK_SRC;
  button.disabled = false;
}

// Flip a card face up 
function flipUpCard(index) {
  state.cards[index].faceUp = true;
  const button = boardEl.querySelector(`.card[data-index="${index}"]`);
  if (!button) return;
  const img = button.querySelector("img");
  if (!img) return;
  animateCardFlip(button);
  img.src = cardFaceSrc(state.cards[index]);
  button.disabled = true;
}

// Handle card click
function handleCardClick(event) {
  if (!state.started || state.locked) return;
  let button = event.target;
  if (button.classList.contains("card")) {
    // clicked the button
  } else if (button.parentElement && button.parentElement.classList.contains("card")) {
    // clicked the img inside the button
    button = button.parentElement;
  } else {
    return;
  }

  const index = Number(button.dataset.index);

  const card = state.cards[index];
  if (!card || card.faceUp || card.matched) return;

  flipUpCard(index);
  state.clicks += 1;
  updateStats();
  checkEndConditions();
  if (state.locked) return;

  state.selected.push(index);
  if (state.selected.length < 2) return;

  state.locked = true;
  const firstIndex = state.selected[0];
  const secondIndex = state.selected[1];
  const firstCard = state.cards[firstIndex];
  const secondCard = state.cards[secondIndex];

  // Check for match by rank
  if (firstCard.rank === secondCard.rank) {
    markPairMatched(firstIndex, secondIndex);
    state.pairs += 1;
    updateStats();
    state.selected = [];
    state.locked = false;
    checkEndConditions();
    return;
  }

  // if not a match flip both cards
  setTimeout(() => {
    flipDownCard(firstIndex);
    flipDownCard(secondIndex);
    state.selected = [];
    state.locked = false;
    checkEndConditions();
  }, 650);
}

// ----------------------------
// anims and effects
// ----------------------------

// create an on click pulse effect at the specified coords
function addCursorPulse(x, y) {
  const pulse = document.createElement("span");
  pulse.className = "pulse";
  pulse.style.left = `${x}px`;
  pulse.style.top = `${y}px`;
  cursorFxLayer.appendChild(pulse);
  setTimeout(() => pulse.remove(), 480);
}

// -------------------------
// accessibility and theme 
// -------------------------

// apply accessibility toggle classes
function applyAccessibilityToggles() {
  if (toggleHighContrastEl.checked) {
    document.body.classList.add("acc-high-contrast");
  } else {
    document.body.classList.remove("acc-high-contrast");
  }
  if (toggleLargeTextEl.checked) {
    document.body.classList.add("acc-large-text");
  } else {
    document.body.classList.remove("acc-large-text");
  }
  if (toggleReducedMotionEl.checked) {
    document.body.classList.add("acc-reduced-motion");
  } else {
    document.body.classList.remove("acc-reduced-motion");
  }
  if (toggleColorModeEl.checked) {
    document.body.classList.add("acc-color-mode");
  } else {
    document.body.classList.remove("acc-color-mode");
  }
  saveAccessibilitySettings();
}

// Apply theme class to body based on selected theme
function applyTheme(themeName) {
  document.body.classList.remove("theme-canterbury", "theme-campus", "theme-seaside", "theme-suits");
  if (themeName !== "default") {
    document.body.classList.add(`theme-${themeName}`);
  }
  saveThemeSettings(themeName);
}

// --------------------------
// localStorage persistence
// --------------------------

// Save current accessibility settings to localStorage
function saveAccessibilitySettings() {
  const settings = {
    highContrast: toggleHighContrastEl.checked,
    largeText: toggleLargeTextEl.checked,
    reducedMotion: toggleReducedMotionEl.checked,
    colorMode: toggleColorModeEl.checked,
  };
  localStorage.setItem("accessibilitySettings", JSON.stringify(settings));
}

// save selected theme to localStorage
function saveThemeSettings(themeName) {
  localStorage.setItem("selectedTheme", themeName);
}

// load accessibility settings from localStorage and apply them
function loadAccessibilitySettings() {
  const saved = localStorage.getItem("accessibilitySettings");
  if (!saved) return;
  const settings = JSON.parse(saved);
  toggleHighContrastEl.checked = settings.highContrast || false;
  toggleLargeTextEl.checked = settings.largeText || false;
  toggleReducedMotionEl.checked = settings.reducedMotion || false;
  toggleColorModeEl.checked = settings.colorMode || false;
  applyAccessibilityToggles();
}

// load theme froom localStorage
function loadThemeSettings() {
  const saved = localStorage.getItem("selectedTheme");
  if (!saved) return;
  themeSelectEl.value = saved;
  applyTheme(saved);
}

// ---------------
// Initialisation
// ---------------

// Initialise the game
function init() {
  loadAccessibilitySettings();
  loadThemeSettings();
  controlsEl.hidden = true;
  statsEl.hidden = true;
  boardPlaceholderEl.hidden = false;
  updateStats();

  // Board size selection
  sizeFieldset.addEventListener("change", (event) => {
    const value = Number(event.target.value);
    if ([2, 4, 6].includes(value)) selectBoardSize(value);
  });

  // Shuffle button
  shuffleBtn.addEventListener("click", handleShuffle);

  // start / quit button
  startBtn.addEventListener("click", () => {
    if (state.started) {
      handleQuit();
    } else {
      handleStart();
    }
  });

  // Card clicks
  boardEl.addEventListener("click", handleCardClick);

  // Play again button
  playAgainBtn.addEventListener("click", () => location.reload());

  // toggles
  toggleHighContrastEl.addEventListener("change", () => {
    if (toggleHighContrastEl.checked) toggleColorModeEl.checked = false;
    applyAccessibilityToggles();
  });

  toggleLargeTextEl.addEventListener("change", applyAccessibilityToggles);
  toggleReducedMotionEl.addEventListener("change", applyAccessibilityToggles);

  toggleColorModeEl.addEventListener("change", () => {
    if (toggleColorModeEl.checked) toggleHighContrastEl.checked = false;
    applyAccessibilityToggles();
  });

  // Theme selection
  themeSelectEl.addEventListener("change", (event) => {
    applyTheme(event.target.value);
  });

  // Click effect
  document.addEventListener("click", (event) => {
    addCursorPulse(event.clientX, event.clientY);
  });
}

init();
