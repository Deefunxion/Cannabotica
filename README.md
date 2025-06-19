# Cannabotica

Modular 8-bit cannabis grow simulation tool with AI-powered agents.

## Structure

- agents/: AI agents
- data/: Input/output files
- scripts/: Pipeline and UI
- docs/: Documentation

## Usage

Run:

```bash
python scripts/run_cannabotica.py
```

This command runs all AI agents to generate plant data and then launches an interactive visualization window.

The visualizer shows a simple schematic of the plant with colored nodes and small shoots. Use the keyboard to step through the growth timeline.

### Visualization Controls

- **Right Arrow / d**: move forward in time
- **Left Arrow / a**: move backward in time

### Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```
