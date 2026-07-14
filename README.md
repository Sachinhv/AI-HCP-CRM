<<<<<<< HEAD
# AI-First CRM — HCP Module: Log Interaction Screen

An AI-first CRM module for pharmaceutical field reps to log, edit, and review
their interactions with Healthcare Professionals (HCPs), either through a
**structured form** or a **conversational AI chat** backed by a **LangGraph**
agent running on **Groq** LLMs.

```
┌───────────────────────────┐        ┌──────────────────────────────┐
│  React + Redux Toolkit    │  REST  │        FastAPI backend        │
│  Log Interaction Screen   │◄──────►│  /hcp  /interaction  /chat    │
│  (form  +  AI chat panel) │        │                                │
└───────────────────────────┘        │   ┌────────────────────────┐  │
                                       │   │  LangGraph ReAct Agent │  │
                                       │   │  (llama-3.3-70b, tool  │  │
                                       │   │   selection)           │  │
                                       │   └───────────┬────────────┘  │
                                       │               │ calls one of  │
                                       │   ┌───────────▼────────────┐  │
                                       │   │ log_interaction         │  │
                                       │   │ edit_interaction        │  │
                                       │   │ summarize_interaction   │  │
                                       │   │ suggest_followup        │  │
                                       │   │ search_history          │  │
                                       │   │ (each also calls        │  │
                                       │   │  gemma2-9b-it for       │  │
                                       │   │  extraction/summarizing)│  │
                                       │   └───────────┬────────────┘  │
                                       │               │               │
                                       │        ┌──────▼──────┐        │
                                       │        │  Postgres   │        │
                                       │        │  (HCP,      │        │
                                       │        │  Interaction)│       │
                                       │        └─────────────┘        │
                                       └────────────────────────────────┘
```

## 1. Why two Groq models?

The assignment asks for `gemma2-9b-it` as the primary model, with
`llama-3.3-70b-versatile` "for context." In practice, Groq's `gemma2-9b-it`
does **not** support native tool/function calling, which the LangGraph
`create_react_agent` needs to decide *which* of the 5 tools to call. So the
two models are split by responsibility:

| Model | Used for | Why |
|---|---|---|
| `llama-3.3-70b-versatile` | The LangGraph agent's tool-routing brain | Supports Groq's native tool-calling API, needed to pick the right tool + arguments from free text. |
| `gemma2-9b-it` | Inside each tool, for entity extraction / summarization (plain text-in, text-out) | Fast and cheap; this kind of call is a simple prompt → JSON/text completion and never needs tool-calling support. |

Both models are configurable via `.env` (`ROUTER_MODEL`, `EXTRACTION_MODEL`)
if you want to swap them.

## 2. LangGraph Agent & Tools

**Role of the agent:** the agent (`backend/app/langgraph/graph.py`) is the
single entry point for the conversational side of the Log Interaction
screen. A rep types a free-text message (e.g. *"Met Dr. Sharma today,
discussed OncoBoost Phase III, she was positive, shared the brochure"*), and
the LangGraph ReAct agent decides which tool the message calls for, invokes
it with the right arguments, and returns a short natural-language
confirmation — while the underlying structured data flows back to the React
form so the rep can review/adjust it before it's finalized.

**The 5 tools** (`backend/app/tools/`):

1. **`log_interaction(raw_text)`** — the primary "structured logging" tool.
   Takes the rep's free-text description, calls `gemma2-9b-it` with an
   extraction prompt to pull out HCP name, interaction type, date/time,
   attendees, topics discussed, materials shared, samples distributed,
   sentiment, outcomes, and follow-up actions as JSON, finds-or-creates the
   HCP record, and inserts a new `Interaction` row in Postgres.

2. **`edit_interaction(user_update, interaction_id?, hcp_name?)`** — lets the
   rep correct something already logged (e.g. *"actually change the
   sentiment to positive"*). Loads the existing record (by ID, or by HCP
   name for their most recent interaction, or the single most recent
   interaction overall if neither is given), sends both the existing JSON
   and the requested change to `gemma2-9b-it`, and applies only the fields
   the LLM says changed.

3. **`summarize_interaction(interaction_id?, hcp_name?)`** — generates a
   short professional summary of a logged interaction for a manager's
   review, via `gemma2-9b-it`.

4. **`suggest_followup(interaction_id?, hcp_name?)`** — asks `gemma2-9b-it`
   for 3 concrete next-step suggestions (e.g. schedule a follow-up, send a
   specific study, add to an advisory board list) based on a logged
   interaction.

5. **`search_history(hcp_name)`** — pulls up to the last 10 interactions for
   an HCP from Postgres and asks `gemma2-9b-it` to summarize the
   relationship history (sentiment trend, topics, open follow-ups).

## 3. The form is read-only by design — the AI chat controls it

The Log Interaction form on the left is **never typed into directly**. Every
field is `readOnly`/`disabled`. The only way any field gets filled in is
through the AI Assistant on the right:

1. The rep describes what happened in plain English in the chat box, e.g.
   *"Today I met with Dr. Smith and discussed Product X efficacy. The
   sentiment was positive, and I shared the brochures."*
2. The LangGraph agent (`llama-3.3-70b-versatile`) routes this to the
   **`log_interaction`** tool, which calls `gemma2-9b-it` to extract the
   structured fields, saves a new row in Postgres, and returns the record.
3. The frontend pushes that record straight into Redux
   (`updateInteraction`), and the read-only form on the left instantly
   reflects it — HCP name, sentiment radio button, topics, materials, etc.
4. If something's wrong, the rep just tells the AI, e.g. *"Actually it was
   Dr. John, and the sentiment was negative"* — the **`edit_interaction`**
   tool updates only those specific fields (both in Postgres and back in
   the form), leaving everything else untouched.

The form's status banner reflects this flow: *"Waiting for the AI
Assistant..."* → *"Draft from AI Assistant"* → *"✅ Saved to CRM (Interaction
#id)"* once `log_interaction` has actually written the row.

## 4. Tech stack

- **Frontend:** React 19 + Vite, Redux Toolkit, Axios, Google Inter font.
- **Backend:** FastAPI, SQLAlchemy 2.0, Pydantic v2.
- **AI:** LangGraph (`create_react_agent`), LangChain (`langchain-groq`),
  Groq SDK.
- **Database:** PostgreSQL (works with any Postgres-compatible instance;
  MySQL would need swapping the driver + minor dialect tweaks).

---

## 5. Setup & run instructions (step by step)

### Prerequisites
- Python 3.11+ (3.12 recommended)
- Node.js 18+ and npm
- PostgreSQL 14+ running locally (or a connection string to any Postgres instance)
- A free Groq API key: https://console.groq.com → API Keys → Create Key

### 5.1 Clone and set up the database
```bash
git clone <your-repo-url>
cd AI-HCP-CRM

# Create the database (adjust user as needed)
psql -U postgres -c "CREATE DATABASE hcp_crm;"
```

### 5.2 Backend setup
```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# then edit .env and set:
#   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/hcp_crm
#   GROQ_API_KEY=<your key from console.groq.com>

# Create the tables
python create_tables.py

# (optional) seed a few demo HCPs so search/history has data right away
python seed_data.py

# Run the API
uvicorn app.main:app --reload --port 8000
```
The backend will be live at `http://127.0.0.1:8000` (interactive API docs
at `http://127.0.0.1:8000/docs`).

### 5.3 Frontend setup
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
The app will be live at `http://127.0.0.1:5173` (Vite's default port).

### 5.4 Try it out
The form on the left is read-only — everything happens through the AI chat
on the right:
- **Log a new interaction:** type something like *"Met Dr. Ananya Sharma today at 3pm,
  discussed OncoBoost Phase III efficacy data, shared the brochure, gave 2
  samples, she seemed positive, follow up in 2 weeks"* in the chat panel on
  the right and hit **Log** — watch the form on the left populate
  automatically.
- Try an edit: *"Actually change the sentiment to neutral"*.
- Try a summary: *"Summarize my last interaction with Dr. Sharma"*.
- Try follow-ups: *"What should I follow up on with Dr. Sharma?"*.
- Try history: *"What's my history with Dr. Sharma?"*.

---

## 6. Project structure
```
AI-HCP-CRM/
├── backend/
│   ├── app/
│   │   ├── config/settings.py         # env var loading
│   │   ├── database/                  # SQLAlchemy engine/session + helpers
│   │   ├── models/                    # HCP, Interaction ORM models
│   │   ├── schemas/                   # Pydantic request/response models
│   │   ├── routers/                   # /hcp, /interaction, /chat endpoints
│   │   ├── services/groq_service.py   # raw Groq completion helper (extraction model)
│   │   ├── tools/                     # the 5 LangGraph tools
│   │   └── langgraph/                 # agent + graph definition (router model)
│   ├── create_tables.py
│   ├── seed_data.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/                # InteractionForm, AIChat, ChatMessage, Navbar
    │   ├── pages/Dashboard.jsx
    │   ├── redux/                     # interactionSlice, chatSlice, store
    │   ├── services/api.js            # axios calls to the backend
    │   └── styles/styles.css
    └── package.json
```

## 7. Security note
`.env` is git-ignored on purpose — never commit real API keys or DB
passwords. Rotate any key that has ever been shared or uploaded elsewhere.

## 8. Known limitations / possible next steps
- The chat agent is stateless per request (no multi-turn memory across
  messages) — "edit the last one" style follow-ups work because
  `edit_interaction` falls back to the most recent record, not because the
  agent remembers the conversation. Adding a LangGraph checkpointer (e.g.
  `MemorySaver`) would enable true multi-turn context.
- HCP search is a simple `ILIKE` query; a production system would likely
  use a dedicated search index for large HCP databases.
- No authentication/authorization layer — out of scope for this
  assignment, but required before any real deployment.
=======
# AI-HCP-CRM
>>>>>>> 81af785ee04a5c541e52fddda8ab7678498bc66d
