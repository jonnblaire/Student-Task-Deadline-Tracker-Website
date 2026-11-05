// ===== SIDEBAR TOGGLE (mobile) =====
function initSidebar() {
  const toggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.overlay');
  if (!toggle || !sidebar) return;

  const close = () => { sidebar.classList.remove('open'); overlay?.classList.remove('show'); };
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay?.classList.toggle('show');
  });
  overlay?.addEventListener('click', close);
  sidebar.querySelectorAll('.nav-item').forEach(a => a.addEventListener('click', close));
}

// ===== MY TASKS: filter logic =====
function initTaskFilters() {
  const search = document.getElementById('taskSearch');
  const subject = document.getElementById('filterSubject');
  const priority = document.getElementById('filterPriority');
  const status = document.getElementById('filterStatus');
  const rows = document.querySelectorAll('#taskTable tbody tr');
  if (!rows.length) return;

  function apply() {
    const q = (search?.value || '').toLowerCase();
    const s = subject?.value || '';
    const p = priority?.value || '';
    const st = status?.value || '';
    rows.forEach(tr => {
      const d = tr.dataset;
      if (!d.name) return;

      const match =
        (!q || d.name.toLowerCase().includes(q)) &&
        (!s || d.subject === s) &&
        (!p || d.priority === p) &&
        (!st || d.status === st);
      tr.style.display = match ? '' : 'none';
    });
  }
  [search, subject, priority, status].forEach(el => el?.addEventListener('input', apply));
}

// ===== SHOW/HIDE PASSWORD =====
function initPasswordToggles() {
  document.querySelectorAll('[data-toggle-pass]').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.togglePass);
      if (!input) return;
      input.type = input.type === 'password' ? 'text' : 'password';
    });
  });
}

// ===== COLOR SWATCHES (subject form) =====
function initColorPicker() {
  document.querySelectorAll('.swatch').forEach(sw => {
    sw.addEventListener('click', () => {
      sw.parentElement.querySelectorAll('.swatch').forEach(s => s.classList.remove('selected'));
      sw.classList.add('selected');
      const hidden = document.getElementById('subjectColor');
      if (hidden) hidden.value = sw.dataset.color;
      const preview = document.getElementById('colorPreview');
      if (preview) preview.style.background = sw.dataset.color;
    });
  });
}

// ===== CALENDAR (Dynamic) =====
function initCalendar() {
  const grid = document.getElementById('calGrid');
  if (!grid) return;

  const monthLabel = document.getElementById('calMonth');
  const detailDate = document.getElementById('calDetailDate');
  const detailList = document.getElementById('calDetailList');
  const prevBtn = document.getElementById('calPrev');
  const nextBtn = document.getElementById('calNext');

  const dataScript = document.getElementById('task-data');
  let tasksData = [];
  if (dataScript) {
    try {
      tasksData = JSON.parse(dataScript.textContent);
    } catch (e) {
      console.error("Error parsing task data", e);
    }
  }

  const tasks = {};
  tasksData.forEach(t => {
    if (!tasks[t.date]) tasks[t.date] = [];
    tasks[t.date].push(t);
  });

  let view = new Date();
  
  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  function render() {
    const y = view.getFullYear(), m = view.getMonth();
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    monthLabel.textContent = monthNames[m] + ' ' + y;

    const first = new Date(y, m, 1).getDay();
    const daysInMonth = new Date(y, m + 1, 0).getDate();
    const today = new Date();
    const isCurrentMonth = today.getFullYear() === y && today.getMonth() === m;

    let html = '';
    let lead = (first + 6) % 7;
    for (let i = 0; i < lead; i++) html += '<div class="cal-cell muted"></div>';

    for (let d = 1; d <= daysInMonth; d++) {
      const dt = new Date(y, m, d);
      const key = iso(dt);
      const dayTasks = tasks[key] || [];
      const dots = dayTasks.map(t => `<span class="cal-dot ${t.priority}"></span>`).join('');
      const todayClass = (isCurrentMonth && d === today.getDate()) ? ' today' : '';
      
      html += `<div class="cal-cell${todayClass}" data-date="${key}">
        <div class="cal-daynum">${d}</div>
        <div class="cal-dots">${dots}</div>
      </div>`;
    }
    grid.innerHTML = html;

    grid.querySelectorAll('.cal-cell:not(.muted)').forEach(cell => {
      cell.addEventListener('click', () => {
        grid.querySelectorAll('.cal-cell').forEach(c => c.classList.remove('selected'));
        cell.classList.add('selected');
        showDetails(cell.dataset.date);
      });
    });
  }

  function showDetails(dateKey) {
    const d = new Date(dateKey + 'T00:00:00');
    const shortMonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    detailDate.textContent = shortMonths[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();

    const list = tasks[dateKey] || [];
    if (!list.length) {
      detailList.innerHTML = '<p style="color:var(--text-2);font-size:13px">No tasks due on this date.</p>';
      return;
    }
    detailList.innerHTML = list.map(t => `
      <div class="deadline-item">
        <div class="deadline-date"><div class="deadline-day">${d.getDate()}</div><div class="deadline-month">${shortMonths[d.getMonth()]}</div></div>
        <div class="deadline-body">
          <div class="deadline-title">${t.title}</div>
          <div class="deadline-meta">${t.subject}</div>
        </div>
      </div>`).join('');
  }

  prevBtn?.addEventListener('click', () => { view = new Date(view.getFullYear(), view.getMonth() - 1, 1); render(); });
  nextBtn?.addEventListener('click', () => { view = new Date(view.getFullYear(), view.getMonth() + 1, 1); render(); });

  render();
}

// ===== BOOT LAHAT DITO =====
document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initTaskFilters();
  initPasswordToggles();
  initColorPicker();
  initCalendar();

  // Auto-hide Django Messages
  const messages = document.getElementById('django-messages');
  if (messages) {
    setTimeout(() => {
      messages.style.transition = 'opacity 0.5s ease';
      messages.style.opacity = '0';
      setTimeout(() => messages.remove(), 500);
    }, 4000);
  }
});