const API = '';

const DIFFICULTY_LABELS = { easy: 'Łatwe', medium: 'Średnie', hard: 'Trudne' };

let allStories = [];
let currentStory = null;
let solutionVisible = false;
let isAsking = false;

// ===== INIT =====

document.addEventListener('DOMContentLoaded', () => {
  loadStories();
  setupEventListeners();
});

function setupEventListeners() {
  document.getElementById('backBtn').addEventListener('click', goBack);
  document.getElementById('revealBtn').addEventListener('click', toggleSolution);
  document.getElementById('randomBtn').addEventListener('click', generateRandom);
  document.getElementById('askBtn').addEventListener('click', askQuestion);
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
      const cls = getAnswerClass(answer);
      loadingEl.className = `msg ai ${cls}`;
      loadingEl.textContent = answer;
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

async function generateRandom() {
  const btn = document.getElementById('randomBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="random-icon">✦</span> Generuję historyjkę...';

  try {
    const res = await fetch(`${API}/api/generate`, { method: 'POST' });
    if (!res.ok) throw new Error('Server error');
    const story = await res.json();
    openStory(story);
  } catch {
    alert('Błąd generowania historyjki. Spróbuj ponownie.');
  }

  btn.disabled = false;
  btn.innerHTML = '<span class="random-icon">✦</span> Wygeneruj losową historyjkę przez AI';
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
  showView('gameView');
  window.scrollTo(0, 0);
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
