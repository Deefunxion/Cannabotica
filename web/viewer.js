export class PlantViewer {
  constructor(canvas, tooltip) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.tooltip = tooltip;
    this.timeline = [];
    this.index = 0;
    this.scale = 1;
    this.offsetX = canvas.width / 2;
    this.offsetY = canvas.height - 50;
    this.dragging = false;
    this.lastX = 0;
    this.lastY = 0;

    this._addInteractions();
  }

  loadTimeline(timeline) {
    if (!Array.isArray(timeline) || !timeline.length) {
      throw new Error('Invalid timeline data');
    }
    this.timeline = timeline;
    this.index = 0;
    this.drawState();
  }

  step(delta) {
    const newIndex = this.index + delta;
    if (newIndex >= 0 && newIndex < this.timeline.length) {
      this.index = newIndex;
      this.drawState(true);
    }
  }

  canvasPos(node) {
    return [
      node.pos[0] * 10 * this.scale + this.offsetX,
      -node.pos[2] * 10 * this.scale + this.offsetY,
    ];
  }

  drawState(animate = false) {
    const state = this.timeline[this.index];
    const nodesById = {};
    state.nodes.forEach((n) => (nodesById[n.id] = n));

    const ctx = this.ctx;
    ctx.save();
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw edges with curves
    ctx.strokeStyle = '#5b4636';
    ctx.lineWidth = 2;
    state.nodes.forEach((n) => {
      if (n.parent && nodesById[n.parent]) {
        const p = nodesById[n.parent];
        const [x1, y1] = this.canvasPos(p);
        const [x2, y2] = this.canvasPos(n);
        ctx.beginPath();
        const cx = (x1 + x2) / 2;
        const cy = (y1 + y2) / 2 - 30 * this.scale;
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(cx, cy, x2, y2);
        ctx.stroke();
      }
    });

    // Draw nodes
    state.nodes.forEach((n) => {
      const [x, y] = this.canvasPos(n);
      let radius = n.type === 'apical' ? 8 : 5;
      radius *= this.scale;
      let color = '#2e7d32';
      if (n.type === 'side') color = '#558b2f';
      if (n.type === 'root_base') color = '#8d6e63';
      if (n.topped) color = '#c62828';
      else if (n.stressed) color = '#ef6c00';
      if (n.vigor !== undefined) {
        const vigor = Math.max(0, Math.min(1, n.vigor));
        const alpha = 0.3 + 0.5 * vigor;
        ctx.fillStyle = color;
        ctx.globalAlpha = alpha;
      } else {
        ctx.fillStyle = color;
      }
      ctx.strokeStyle = '#000';
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Training icons
      if (n.training_state) {
        ctx.fillStyle = '#000';
        ctx.font = `${12 * this.scale}px sans-serif`;
        const icon = n.training_state === 'topped'
          ? '\u2702'
          : n.training_state === 'supercropped'
          ? '\u26A1'
          : 'F';
        ctx.fillText(icon, x + radius, y - radius);
      }
    });

    ctx.restore();
    this.canvas.dataset.day = state.day;
  }

  _addInteractions() {
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoom = e.deltaY < 0 ? 1.1 : 0.9;
      this.scale = Math.max(0.2, Math.min(5, this.scale * zoom));
      this.drawState();
    });

    this.canvas.addEventListener('mousedown', (e) => {
      this.dragging = true;
      this.lastX = e.offsetX;
      this.lastY = e.offsetY;
    });
    window.addEventListener('mousemove', (e) => {
      if (!this.dragging) return;
      const dx = e.offsetX - this.lastX;
      const dy = e.offsetY - this.lastY;
      this.lastX = e.offsetX;
      this.lastY = e.offsetY;
      this.offsetX += dx;
      this.offsetY += dy;
      this.drawState();
    });
    window.addEventListener('mouseup', () => {
      this.dragging = false;
    });

    this.canvas.addEventListener('mousemove', (e) => {
      const state = this.timeline[this.index];
      if (!state) return;
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const hit = state.nodes.find((n) => {
        const [nx, ny] = this.canvasPos(n);
        const r = (n.type === 'apical' ? 8 : 5) * this.scale;
        return Math.hypot(nx - x, ny - y) <= r + 2;
      });
      if (hit) {
        this.tooltip.classList.remove('hidden');
        this.tooltip.style.left = `${e.clientX + 10}px`;
        this.tooltip.style.top = `${e.clientY + 10}px`;
        this.tooltip.textContent = `${hit.id} (day ${hit.age_days})`;
      } else {
        this.tooltip.classList.add('hidden');
      }
    });
  }
}
