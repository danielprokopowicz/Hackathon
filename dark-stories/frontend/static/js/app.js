const API = '';

const DIFFICULTY_LABELS = { easy: 'Łatwe', medium: 'Średnie', hard: 'Trudne' };

const HINTS_PER_DIFFICULTY = { easy: 5, medium: 3, hard: 1 };

let allStories = [];
let currentStory = null;
let solutionVisible = false;
let isAsking = false;
let hintsUsed = 0;
let hintsMax = 3;
let gameOver = false;

// ===== INIT =====

document.addEventListener('DOMContentLoaded', () => {
  loadStories();
  setupEventListeners();
});

function setupEventListeners() {
  document.getElementById('backBtn').addEventListener('click', goBack);
  document.getElementById('revealBtn').addEventListener('click', toggleSolution);
  document.getElementById('askBtn').addEventListener('click', askQuestion);
  document.getElementById('hintBtn').addEventListener('click', requestHint);
  document.getElementById('giveUpBtn').addEventListener('click', giveUp);
  document.getElementById('questionInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') askQuestion();
  });
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderStories(tab.dataset.filter);
    });
  });
}

// ===== API CALLS =====

async function loadStories() {
  try {
    const res = await fetch(`${API}/api/stories`);
    allStories = await res.json();
    renderStories('all');
  } catch (e) {
    document.getElementById('storiesGrid').innerHTML =
      '<div class="loading-state">Błąd ładowania historyjek. Sprawdź czy serwer działa.</div>';
  }
}

async function askQuestion() {
  const input = document.getElementById('questionInput');
  const question = input.value.trim();
  if (!question || !currentStory || isAsking) return;

  isAsking = true;
  const btn = document.getElementById('askBtn');
  btn.disabled = true;

  removeEmptyState();
  appendMessage(question, 'user');
  input.value = '';

  const loadingId = 'msg-' + Date.now();
  appendMessage('Zastanawiam się...', 'ai loading', loadingId);
  scrollMessages();

  const body = {
    story_id: currentStory.id,
    question,
  };

  if (currentStory.id === 'random') {
    body.story_data = currentStory;
  }

  try {
    const res = await fetch(`${API}/api/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) throw new Error('Server error');
    const data = await res.json();
    const answer = data.answer;

    const loadingEl = document.getElementById(loadingId);
    if (loadingEl) {
      if (data.solved) {
        loadingEl.className = 'msg ai solved';
        loadingEl.textContent = 'Brawo! Rozwiązałeś zagadkę!';
        showWin();
      } else {
        const cls = getAnswerClass(answer);
        loadingEl.className = `msg ai ${cls}`;
        loadingEl.textContent = answer;
      }
    }
  } catch {
    const loadingEl = document.getElementById(loadingId);
    if (loadingEl) {
      loadingEl.className = 'msg ai no';
      loadingEl.textContent = 'Błąd połączenia z serwerem.';
    }
  }

  isAsking = false;
  btn.disabled = false;
  scrollMessages();
}

async function requestHint() {
  if (!currentStory || isAsking) return;
  if (hintsUsed >= hintsMax) return;

  isAsking = true;
  const btn = document.getElementById('hintBtn');
  btn.disabled = true;

  removeEmptyState();
  const loadingId = 'hint-' + Date.now();
  appendMessage('Szukam wskazówki...', 'ai loading', loadingId);
  scrollMessages();

  const body = {
    story_id: currentStory.id,
    hint_num: hintsUsed + 1,
    max_hints: hintsMax,
  };
  if (currentStory.id === 'random') {
    body.story_data = currentStory;
  }

  try {
    const res = await fetch(`${API}/api/hint`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('Server error');
    const data = await res.json();
    const el = document.getElementById(loadingId);
    if (el) {
      el.className = 'msg ai hint';
      el.textContent = data.hint;
    }
    hintsUsed++;
    updateHintBtn();
  } catch {
    const el = document.getElementById(loadingId);
    if (el) {
      el.className = 'msg ai no';
      el.textContent = 'Błąd pobierania wskazówki.';
    }
  }

  isAsking = false;
  if (hintsUsed < hintsMax) btn.disabled = false;
  scrollMessages();
}

function updateHintBtn() {
  const btn = document.getElementById('hintBtn');
  const countEl = document.getElementById('hintCount');
  const remaining = hintsMax - hintsUsed;
  countEl.textContent = `${remaining} pozostało`;
  if (remaining <= 0) {
    btn.disabled = true;
  }
}

const CATEGORY_LABELS = {
  dark: 'Mroczne historie',
  pko: 'PKO XP Gaming',
  tauron: 'Tauron AI',
};

async function generateRandom(category = 'dark') {
  const btns = document.querySelectorAll('.gen-btn');
  btns.forEach(b => { b.disabled = true; });
  const activeBtn = document.querySelector(`.gen-${category}`);
  if (activeBtn) {
    const icon = activeBtn.querySelector('.gen-icon');
    if (icon) icon.textContent = '⏳';
  }

  try {
    const res = await fetch(`${API}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category }),
    });
    if (!res.ok) throw new Error('Server error');
    const story = await res.json();
    openStory(story);
  } catch {
    alert('Błąd generowania historyjki. Spróbuj ponownie.');
  }

  btns.forEach(b => { b.disabled = false; });
  const icons = { dark: '🌑', pko: '🎮', tauron: '⚡' };
  if (activeBtn) {
    const icon = activeBtn.querySelector('.gen-icon');
    if (icon) icon.textContent = icons[category] || '✦';
  }
}

// ===== RENDER =====

function renderStories(filter = 'all') {
  const grid = document.getElementById('storiesGrid');
  const filtered = filter === 'all' ? allStories : allStories.filter(s => s.difficulty === filter);

  if (!filtered.length) {
    grid.innerHTML = '<div class="loading-state">Brak historyjek w tej kategorii.</div>';
    return;
  }

  grid.innerHTML = filtered.map(s => `
    <div class="story-card ${s.difficulty}" data-id="${s.id}" role="button" tabindex="0">
      <span class="badge ${s.difficulty}">${DIFFICULTY_LABELS[s.difficulty]}</span>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(s.story.substring(0, 90))}...</p>
    </div>
  `).join('');

  grid.querySelectorAll('.story-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = parseInt(card.dataset.id);
      const story = allStories.find(s => s.id === id);
      if (story) openStory(story);
    });
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') card.click();
    });
  });
}

function openStory(story) {
  currentStory = story;
  solutionVisible = false;
  hintsUsed = 0;
  hintsMax = HINTS_PER_DIFFICULTY[story.difficulty] ?? 3;
  gameOver = false;

  document.getElementById('gameBadge').className = `badge ${story.difficulty}`;
  document.getElementById('gameBadge').textContent = DIFFICULTY_LABELS[story.difficulty] || '—';
  document.getElementById('gameTitle').textContent = story.title;
  document.getElementById('gameStory').textContent = story.story;
  document.getElementById('solutionBox').textContent = story.solution || '(rozwiązanie niedostępne)';
  document.getElementById('solutionBox').classList.remove('visible');
  document.getElementById('revealBtn').textContent = 'Pokaż rozwiązanie';
  document.getElementById('revealBtn').classList.remove('revealed');

  const messages = document.getElementById('messages');
  messages.innerHTML = `
    <div class="empty-state">
      <span>Zacznij zadawać pytania, aby rozwikłać zagadkę</span>
    </div>
  `;

  document.getElementById('questionInput').value = '';
  document.getElementById('questionInput').disabled = false;
  document.getElementById('askBtn').disabled = false;
  document.getElementById('hintBtn').disabled = false;
  document.getElementById('giveUpBtn').disabled = false;
  updateHintBtn();
  showView('gameView');
  window.scrollTo(0, 0);
}

function showWin() {
  if (gameOver) return;
  gameOver = true;
  const panel = document.querySelector('.qa-panel');
  const input = document.getElementById('questionInput');
  const btn = document.getElementById('askBtn');
  input.disabled = true;
  btn.disabled = true;
  document.getElementById('hintBtn').disabled = true;
  document.getElementById('giveUpBtn').disabled = true;

  const win = document.createElement('div');
  win.className = 'win-banner';
  win.innerHTML = `
    <div class="win-title">Zagadka rozwiązana</div>
    <div class="win-sub">Odkryłeś prawdę kryjącą się za historią.</div>
    <button class="win-btn" onclick="document.getElementById('revealBtn').click()">Pokaż rozwiązanie</button>
  `;
  panel.appendChild(win);
}

function giveUp() {
  if (!currentStory || gameOver) return;
  gameOver = true;

  const input = document.getElementById('questionInput');
  const askBtn = document.getElementById('askBtn');
  const hintBtn = document.getElementById('hintBtn');
  const giveUpBtn = document.getElementById('giveUpBtn');
  input.disabled = true;
  askBtn.disabled = true;
  hintBtn.disabled = true;
  giveUpBtn.disabled = true;

  if (!solutionVisible) toggleSolution();

  const panel = document.querySelector('.qa-panel');
  const lose = document.createElement('div');
  lose.className = 'lose-banner';
  lose.innerHTML = `
    <div class="lose-title">Poddałeś się</div>
    <div class="lose-sub">Tym razem zagadka okazała się zbyt trudna. Rozwiązanie zostało ujawnione.</div>
    <button class="lose-btn" onclick="document.getElementById('revealBtn').click()">Pokaż rozwiązanie</button>
  `;
  panel.appendChild(lose);
}

function goBack() {
  currentStory = null;
  showView('listView');
}

function toggleSolution() {
  solutionVisible = !solutionVisible;
  const box = document.getElementById('solutionBox');
  const btn = document.getElementById('revealBtn');
  box.classList.toggle('visible', solutionVisible);
  btn.textContent = solutionVisible ? 'Ukryj rozwiązanie' : 'Pokaż rozwiązanie';
  btn.classList.toggle('revealed', solutionVisible);
}

// ===== HELPERS =====

function showView(id) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function appendMessage(text, classes, id = null) {
  const messages = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = `msg ${classes}`;
  div.textContent = text;
  if (id) div.id = id;
  messages.appendChild(div);
}

function removeEmptyState() {
  const empty = document.querySelector('#messages .empty-state');
  if (empty) empty.remove();
}

function scrollMessages() {
  const messages = document.getElementById('messages');
  messages.scrollTop = messages.scrollHeight;
}

function getAnswerClass(answer) {
  const lower = answer.toLowerCase();
  if (lower.startsWith('tak i')) return 'partial';
  if (lower.startsWith('tak')) return 'yes';
  if (lower.startsWith('nie ma')) return 'partial';
  if (lower.startsWith('nie')) return 'no';
  return 'partial';
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
