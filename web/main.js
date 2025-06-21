import { PlantViewer } from './viewer.js';

const fileInput = document.getElementById('fileInput');
const loader = document.getElementById('loader');
const controls = document.getElementById('controls');
const dayRange = document.getElementById('dayRange');
const dayLabel = document.getElementById('dayLabel');
const exportBtn = document.getElementById('exportBtn');
const detailToggle = document.getElementById('toggleDetails');
const canvas = document.getElementById('canvas');
const tooltip = document.getElementById('tooltip');

const viewer = new PlantViewer(canvas, tooltip);
let timeline = [];

function handleFiles(files) {
  const file = files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    try {
      timeline = JSON.parse(e.target.result);
      if (!Array.isArray(timeline)) {
        alert('Invalid JSON format: expected an array');
        return;
      }
      dayRange.max = timeline.length - 1;
      dayRange.value = 0;
      dayLabel.textContent = timeline[0].day;
      controls.classList.remove('hidden');
      loader.classList.add('hidden');
      viewer.loadTimeline(timeline);
    } catch (err) {
      alert('Failed to parse JSON: ' + err.message);
    }
  };
  reader.readAsText(file);
}

fileInput.addEventListener('change', () => handleFiles(fileInput.files));
loader.addEventListener('dragover', evt => { evt.preventDefault(); loader.classList.add('dragover'); });
loader.addEventListener('dragleave', () => loader.classList.remove('dragover'));
loader.addEventListener('drop', evt => {
  evt.preventDefault();
  loader.classList.remove('dragover');
  if (evt.dataTransfer.files.length) handleFiles(evt.dataTransfer.files);
});

dayRange.addEventListener('input', () => {
  dayLabel.textContent = timeline[dayRange.value].day;
  viewer.index = +dayRange.value;
  viewer.drawState(true);
});

window.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') {
    viewer.step(1);
    dayRange.value = viewer.index;
    dayLabel.textContent = timeline[viewer.index].day;
  } else if (e.key === 'ArrowLeft') {
    viewer.step(-1);
    dayRange.value = viewer.index;
    dayLabel.textContent = timeline[viewer.index].day;
  }
});

exportBtn.addEventListener('click', () => {
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/png');
  link.download = `plant_day_${canvas.dataset.day}.png`;
  link.click();
});

// detail toggle just redraws currently; viewer already shows details by default
if (detailToggle) {
  detailToggle.addEventListener('change', () => viewer.drawState());
}
