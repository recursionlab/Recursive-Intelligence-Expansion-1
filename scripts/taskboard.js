// Dynamic MoC Taskboard
async function loadTaskboard() {
  const response = await fetch('/taskboard');
  const data = await response.json();
  const kanban = document.getElementById('taskboard');
  kanban.innerHTML = '';
  for (const [folder, jobs] of Object.entries(data.taskboard)) {
    const col = document.createElement('div');
    col.className = 'folder';
    col.innerHTML = `<h4>${folder}</h4>`;
    jobs.forEach(job => {
      const item = document.createElement('div');
      item.className = 'job';
      item.innerHTML = `
        <strong>${job.title}</strong><br>${job.desc}
        <select onchange="updateJob(${job.id}, this.value)">
          <option ${job.folder === 'Inbox' ? 'selected' : ''}>Inbox</option>
          <option ${job.folder === 'My Jobs' ? 'selected' : ''}>My Jobs</option>
          <option ${job.folder === 'Active' ? 'selected' : ''}>Active</option>
          <option ${job.folder === 'Done' ? 'selected' : ''}>Done</option>
        </select>
      `;
      col.appendChild(item);
    });
    kanban.appendChild(col);
  }
}

async function updateJob(id, folder) {
  const apiKey = localStorage.getItem('api_key') || prompt('API Key:');
  await fetch('/taskboard/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: new URLSearchParams({id, folder, api_key: apiKey})
  });
  loadTaskboard();
}

