# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Stats Visualizer** is a single-file interactive visualization tool for mathematical probability distributions. It's built with HTML, CSS, and JavaScript, with no build process or external dependencies beyond Plotly.js (loaded from CDN).

The tool provides interactive exploration of five probability distributions:
- Normal (Gaussian)
- Uniform
- Exponential
- Binomial
- Poisson

## File Structure

### distributions.html (848 lines)

The entire project is contained in one file with three sections:

#### 1. HTML Structure (lines 1-271)
- `<head>`: Metadata, Plotly.js script tag, and embedded styles
- `<body>`: Container with header, tab buttons, and 5 content sections (one per distribution)

Each distribution section (`<div id="normal">`, etc.) contains:
- Description box explaining the distribution
- Two-column layout with:
  - Plot container (left): `<div id="plot-{name}" class="chart"></div>`
  - Controls (right): Sliders for parameters and properties display box

#### 2. CSS (lines 8-270, embedded in `<style>`)
- Dark theme with cyan (#00d4ff) accents
- Responsive grid layout with breakpoints at 1024px and 768px
- Slider styling with gradient thumb and glow effects
- Classes: `.tabs`, `.tab-button`, `.content`, `.distribution-card`, `.row`, `.chart`, `.controls`, `.slider-container`, `.properties`, `.formula`

#### 3. JavaScript (lines 585-847, embedded in `<script>`)
- **Math utilities**: `factorial()`, `combination()`, `normalPDF()`, `binomialPMF()`, `poissonPMF()`
- **Tab control**: `switchTab(tabName)` - handles tab switching and triggering distribution updates
- **Distribution functions**: Five `update{Name}()` functions that:
  1. Read slider values from DOM
  2. Calculate distribution properties
  3. Update property display elements
  4. Generate data arrays and call Plotly.newPlot()
- **Event listeners**: Load and resize handlers

## Development Workflow

To develop or modify this project:

```bash
# 1. Open the file in your browser (no server needed)
open distributions.html
# or
firefox distributions.html
```

2. Edit the HTML/CSS/JavaScript in your editor
3. Refresh the browser to see changes
4. No build, compile, or test commands required

## Common Development Tasks

### Adding a New Distribution

1. **Add HTML section** (after line 582):
   ```html
   <!-- Distribution Name -->
   <div id="dist-id" class="content">
       <div class="distribution-card">
           <div class="description">Description here</div>
           <div class="row">
               <div class="plot-container">
                   <div id="plot-dist-id" class="chart"></div>
               </div>
               <div class="controls">
                   <!-- Sliders and properties -->
               </div>
           </div>
       </div>
   </div>
   ```

2. **Add tab button** (around line 280):
   ```html
   <button class="tab-button" onclick="switchTab('dist-id')">Name</button>
   ```

3. **Add update function** (in JavaScript, around line 630):
   ```javascript
   function updateDistName() {
       const param = parseFloat(document.getElementById('param').value);
       // Calculate properties and update DOM elements
       const x = [], y = [];
       // Generate data points
       Plotly.newPlot('plot-dist-id', [trace], layout, { responsive: true });
   }
   ```

4. **Register in updateDistribution()** (around line 635):
   ```javascript
   else if (type === 'dist-id') updateDistName();
   ```

### Modifying Distribution Parameters

- **Slider range/step**: Edit `min`, `max`, `step` attributes on `<input type="range">` elements (lines 308-318, 371-381, etc.)
- **Display formatting**: Update `.toFixed()` calls in the update functions
- **Formula display**: Edit the formula text in `.formula` divs

### Changing Colors or Theme

All theme colors are defined in CSS:
- Primary accent: `#00d4ff` (cyan)
- Background: `#1e1e1e`, `#2d2d2d` (dark grays)
- Text: `#e0e0e0`, `#c0c0c0`, `#000` (light/dark)
- Secondary: `#ff6b6b` (red), `#4ecdc4` (teal)

Update in the `<style>` section (lines 8-270).

## Architecture & Patterns

### Parameter Binding
Each distribution has a pattern where:
1. HTML input element has an `id` (e.g., `id="mu"`)
2. Slider has `oninput="updateDistribution('normal')"`
3. Update function reads with `document.getElementById(id).value`
4. Display elements updated directly via `textContent`

### Plotly Configuration
All distributions use this pattern:
```javascript
const trace = {
    x: xArray,
    y: yArray,
    type: 'scatter' // or 'bar'
    // ... styling
};
const layout = {
    plot_bgcolor: 'rgba(0,0,0,0.1)',
    paper_bgcolor: 'rgba(0,0,0,0)',
    // ... axes and margins
};
Plotly.newPlot('plot-id', [trace], layout, { responsive: true });
```

## Dependencies

- **Plotly.js v2.26.0**: Loaded from CDN (line 7)
  - Used for all chart rendering
  - No local installation needed
  - Responsive mode enabled for window resize handling

No npm packages, Python dependencies, or build tools required.
