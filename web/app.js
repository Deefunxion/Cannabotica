const fileInput = document.getElementById('fileInput');
const loader = document.getElementById('loader');
const controls = document.getElementById('controls');
const dayRange = document.getElementById('dayRange');
const dayLabel = document.getElementById('dayLabel');
const exportBtn = document.getElementById('exportBtn');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let timeline = [];
let nodesById = {};

function handleFiles(files) {
  const file = files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    try {
      timeline = JSON.parse(e.target.result);
      if (!Array.isArray(timeline)) {
        alert('Invalid JSON format: expected a list');
        return;
      }
      dayRange.max = timeline.length - 1;
      dayRange.value = 0;
      dayLabel.textContent = timeline[0].day;
      controls.classList.remove('hidden');
      loader.classList.add('hidden');
      drawState(0);
    } catch (err) {
      alert('Failed to parse JSON: ' + err.message);
    }
  };
  reader.readAsText(file);
}

function curve(ctx, x1, y1, x2, y2) {
  const cx = (x1 + x2) / 2;
  const cy = (y1 + y2) / 2 - 20;
  ctx.moveTo(x1, y1);
  ctx.quadraticCurveTo(cx, cy, x2, y2);
}

function drawState(index) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const state = timeline[index];
  dayLabel.textContent = state.day;
  nodesById = {};
  state.nodes.forEach(n => { nodesById[n.id] = n; });

  // Draw edges first
  ctx.strokeStyle = '#555';
  ctx.lineWidth = 2;
  state.nodes.forEach(n => {
    if (n.parent && nodesById[n.parent]) {
      const parent = nodesById[n.parent];
      const x1 = parent.pos[0] * 10 + canvas.width / 2;
      const y1 = canvas.height - parent.pos[2] * 10 - 50;
      const x2 = n.pos[0] * 10 + canvas.width / 2;
      const y2 = canvas.height - n.pos[2] * 10 - 50;
      ctx.beginPath();
      curve(ctx, x1, y1, x2, y2);
      ctx.stroke();
    }
  });

  // Draw nodes
  state.nodes.forEach(n => {
    const x = n.pos[0] * 10 + canvas.width / 2;
    const y = canvas.height - n.pos[2] * 10 - 50;
    let color = n.type === 'apical' ? 'forestgreen' : 'royalblue';
    if (n.topped) color = 'crimson';
    else if (n.stressed) color = 'darkorange';
    const radius = n.type === 'apical' ? 9 : 6;
    ctx.fillStyle = color;
    ctx.strokeStyle = 'black';
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    if (n.vigor !== undefined) {
      ctx.beginPath();
      ctx.globalAlpha = 0.1 * n.vigor;
      ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1.0;
    }
  });
}

fileInput.addEventListener('change', () => handleFiles(fileInput.files));
loader.addEventListener('dragover', evt => {
  evt.preventDefault();
  loader.classList.add('dragover');
});
loader.addEventListener('dragleave', () => loader.classList.remove('dragover'));
loader.addEventListener('drop', evt => {
  evt.preventDefault();
  loader.classList.remove('dragover');
  if (evt.dataTransfer.files.length) handleFiles(evt.dataTransfer.files);
});

dayRange.addEventListener('input', () => {
  drawState(+dayRange.value);
});

exportBtn.addEventListener('click', () => {
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/png');
  link.download = `plant_day_${dayLabel.textContent}.png`;
  link.click();
});
