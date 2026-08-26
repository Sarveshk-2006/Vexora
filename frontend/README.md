# FRAUDOSCOPE — Frontend Command Center

> **Stack:** React 18, TypeScript, Vite, Tailwind CSS, React Flow, Recharts, Framer Motion  
> **Status:** Phase 1 Foundation Shell Established

---

## Overview

The `frontend/` directory contains the React command center interface for monitoring payment digital twin simulations, visualizing attack evolution graphs, and inspecting model defense gaps.

---

## Local Setup

1. **Install Node.js 20+**
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Set Environment Variables:**
   Copy `.env.example` or create `.env.local`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```
4. **Start Development Server:**
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## Development Scripts

```bash
# Start Vite dev server
npm run dev

# Run Vitest suite
npm run test

# Build production bundle
npm run build

# Preview production build
npm run preview
```
