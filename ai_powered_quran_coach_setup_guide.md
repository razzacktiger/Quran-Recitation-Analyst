# AI‑Powered Quran Coach Setup Guide

This document has **two** sections:

1. **n8n‑Based Prototype** (low‑code)
2. **Full‑Stack Custom Code**

Use it in your Cursor MD environment so your agent can guide each step.

---

## 1. n8n‑Based Prototype

### 🎯 Overview

- **Orchestrate** data entry, AI analysis, and notifications in n8n
- **Store** all records + insights in a Postgres (or MySQL) database
- **Visualize** via a simple Next.js dashboard

### 🔧 Prerequisites

1. **n8n Cloud** account (or self‑hosted n8n)
2. **Postgres** database (e.g. Supabase) with your schema
3. **OpenAI API key** (for AI calls)
4. **Next.js** CLI installed (`npm install -g create-next-app`)

---

### A. Database Setup

1. Create a new Postgres database.
2. Run SQL to create tables:
   ```sql
   -- sessions
   CREATE TABLE sessions (
     id SERIAL PRIMARY KEY,
     user_id TEXT,
     timestamp TIMESTAMPTZ,
     duration INT,
     performance_score FLOAT,
     notes TEXT
   );
   -- portion_details
   CREATE TABLE portion_details (
     id SERIAL PRIMARY KEY,
     session_id INT REFERENCES sessions(id),
     portion_type TEXT,
     reference TEXT,
     recency_category TEXT
   );
   -- test_types
   CREATE TABLE test_types (
     id SERIAL PRIMARY KEY,
     session_id INT REFERENCES sessions(id),
     category TEXT,
     description TEXT,
     success_rate FLOAT
   );
   -- learning_methods
   CREATE TABLE learning_methods (
     id SERIAL PRIMARY KEY,
     session_id INT REFERENCES sessions(id),
     method_type TEXT,
     details TEXT
   );
   -- mistakes
   CREATE TABLE mistakes (
     id SERIAL PRIMARY KEY,
     session_id INT REFERENCES sessions(id),
     location TEXT,
     error_category TEXT,
     error_subcategory TEXT,
     details TEXT,
     correction_method TEXT,
     resolution_status TEXT
   );
   -- insights
   CREATE TABLE insights (
     id SERIAL PRIMARY KEY,
     user_id TEXT,
     generated_at TIMESTAMPTZ,
     summary TEXT,
     next_actions JSONB
   );
   ```

---

### B. n8n Workflows

#### 1. Data Entry Workflow

- **Trigger:** HTTP Webhook (e.g. `POST /n8n/webhook/session`)
- **Nodes:**
  1. **Webhook** — receive JSON payload
  2. **Set** — map incoming fields to DB columns
  3. **Postgres** — insert into `sessions`, `portion_details`, `mistakes`, etc.
  4. **Respond** — return success JSON

#### 2. AI Analysis Workflow

- **Trigger:** Cron node (e.g. every night at 2 AM)
- **Nodes:**
  1. **Postgres** — fetch all sessions & mistakes for the past week
  2. **Function** or **HTTP Request** — call OpenAI:
     - **Prompt:** summarize mistake patterns, suggest focus areas, generate next‑review dates
  3. **Postgres** — insert into `insights` table
  4. **Respond** — optionally notify via email/chat

#### 3. Notification Workflow (optional)

- **Trigger:** New row in `insights` (via Postgres Trigger + Webhook)
- **Nodes:**
  1. **Webhook** — catch trigger
  2. **Email** or **Telegram** node — send summary to user

---

### C. Next.js Dashboard

1. **Create app:**
   ```bash
   npx create-next-app quran-coach-dashboard
   cd quran-coach-dashboard
   npm install pg chart.js react-chartjs-2
   ```
2. **Configure DB:** in `next.config.js` or via environment variables (`DATABASE_URL`)
3. **Fetch data:**
   - In `pages/index.js`, use `getServerSideProps` to query `sessions`, `insights`
4. **Visualize:**
   - Use `react-chartjs-2` for line/bar charts
   - Show:
     - **Progress over time** (sessions vs. performance\_score)
     - **Mistake heatmap** (count by error\_category & surah)
     - **Upcoming reviews** from `insights.next_actions`
5. **Deploy:** Vercel or Netlify, configure env vars

---

## 2. Full‑Stack Custom Code

### 🎯 Overview

- **API** (Node.js/Express or Python/FastAPI)
- **DB** with same schema
- **AI Agent** module for categorization & coaching
- **Front‑end** (Next.js)

### 🔧 Prerequisites

1. **Node.js** (v16+) or **Python** (3.9+)
2. **Postgres** database (Supabase or similar)
3. **OpenAI API key**
4. **Redis** (optional, for job queue)

---

### A. Backend Setup

#### 1. Initialize Project

- **Node.js**:
  ```bash
  mkdir quran-coach-api && cd quran-coach-api
  npm init -y
  npm install express pg prisma openai bullmq
  npx prisma init
  ```
- **Python**:
  ```bash
  mkdir quran_coach_api && cd quran_coach_api
  python -m venv venv && source venv/bin/activate
  pip install fastapi uvicorn sqlalchemy psycopg2-binary openai aiojobs
  ```

#### 2. ORM & Schema

- Copy your SQL schema into Prisma (`prisma/schema.prisma`) or SQLAlchemy models.
- **Prisma example**:
  ```prisma
  datasource db { provider = "postgresql" url = env("DATABASE_URL") }
  generator client { provider = "prisma-client-js" }

  model Session { id Int @id @default(autoincrement()) userId String timestamp DateTime … }
  // define other models similarly…
  ```

#### 3. API Routes

- **POST /session**
  - Accept JSON or multipart (for audio)
  - If audio: call Whisper (OpenAI) to transcribe
  - Validate fields, insert into DB (sessions + related tables)
  - Return `{ success: true, sessionId }`
- **GET /insights/****:userId**
  - Query `insights` table (or compute on‑the‑fly)
  - Return summaries & next actions

#### 4. AI Agent Module

- **File:** `src/aiAgent.js` (Node) or `ai_agent.py` (Python)
- **Functions:**
  1. `categorizeMistakes(mistakesList)`: map raw text → error\_category/subcategory
  2. `generateInsights(userId)`: fetch recent data, craft prompt, call OpenAI, parse response
  3. `scheduleReviews(sessions)`: apply forgetting‑curve logic (e.g. review after 1d, 3d, 7d)

#### 5. Scheduler & Queue

- Use **BullMQ** (Node) or **aiojobs** / **APScheduler** (Python)
- **Weekly Job:** enqueue `generateInsights(userId)` for each active user

---

### B. Front‑End Setup

1. **Create Next.js App** (same as n8n guide)
2. **Install API client**:
   ```bash
   npm install axios react-chartjs-2 chart.js
   ```
3. **Environment:** add `NEXT_PUBLIC_API_URL`
4. **Pages & Components:**
   - **ChatWidget**: UI for “I recited Surah 2:1–10, mistakes on 2:5”
     - On submit: `POST ${API_URL}/session`
   - **Dashboard**:
     - Fetch `GET ${API_URL}/insights/${userId}`
     - Render charts & coach panel
5. **Voice Input (optional):**
   - Use browser’s `MediaRecorder` API to record audio
   - Send blob to `POST /session`

---

### C. Deployment & Next Steps

1. **Backend:**
   - Deploy to Heroku, Railway, or Render
   - Set env vars: `DATABASE_URL`, `OPENAI_API_KEY`, `REDIS_URL`
2. **Front‑end:**
   - Deploy to Vercel/Netlify
3. **Monitoring:**
   - Add basic logs around AI calls and DB errors
4. **Iterate:**
   - Gather user feedback
   - Refine prompts, improve UX, add access control

---

> **Tip:** Start with the n8n prototype to validate your data flows and AI prompts. Once you’re confident in the core logic, use the custom‑code section as your blueprint to build a production‑grade app.

Good luck building your AI‑powered Quran memorization coach!

