
# Quick Task Bot 🤖🗒️

A Telegram chatbot that uses **SpaCy** to extract tasks and due dates from natural language.
Example: “remind me to finish the physics lab by Friday 5pm”.

## What problem does this solve?
Turning casual chat into a to-do list is tedious. This bot lets you type naturally and turns it into structured tasks with optional due dates, right inside Telegram.

## How it works (NLP)
- Uses SpaCy's `en_core_web_sm` model for **Named Entity Recognition** (NER) and part-of-speech parsing.
- Detects `DATE` and `TIME` entities for due dates.
- Guesses the task **description** by extracting a verb phrase (root verb subtree), with fallbacks.
- Saves tasks per-user in a simple JSON store (`tasks_store.json`).

## Features
- Add tasks by just messaging the bot in plain English.
- `/list` to view tasks.
- `/done <number>` to mark as complete.
- `/clear` to wipe your list.
- Light-weight; no external APIs required.

---

## Setup — Step by Step

### 1) Create your bot in Telegram
1. Open Telegram and search for **BotFather**.
2. Send `/newbot` and follow the prompts (pick a name and a username).
3. Copy the **HTTP API token** you receive; you'll need it below.

### 2) Clone this repo (or unzip the release)
```bash
git clone https://github.com/yourusername/quick-task-bot.git
cd quick-task-bot
```
(If you downloaded the ZIP from the course, just unzip and `cd` into the folder.)

### 3) Create & activate a virtual environment
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```

### 5) Install SpaCy English model
```bash
python -m spacy download en_core_web_sm
```

### 6) Add your Telegram token
- Copy `.env.example` to `.env` and paste your token:
```
TELEGRAM_TOKEN=123456:ABC-your-token-here
```

### 7) Run the bot
```bash
python bot.py
```
You should see `Bot is running. Press Ctrl+C to stop.`

### 8) Talk to your bot
In Telegram, open your bot and try messages like:
- `remind me to finish the report by Friday 5pm`
- `call Alice tomorrow`
- `submit assignment on 10 Oct`
- Then use `/list` and `/done 1`

---

## Verifying it works
1. Send: `remind me to email Prof Naidoo by Monday 9am`  
   Expect: `Added: email Prof Naidoo (due: Monday 9am)`
2. Send: `/list`  
   Expect a numbered list with your task.
3. Send: `/done 1`  
   Expect confirmation that task 1 is removed.
4. Restart the bot and send `/list` — tasks persist in `tasks_store.json`.

---

## Limitations
- **Heuristic parsing**: The task description & due date extraction uses simple heuristics and SpaCy’s small model; phrasing that’s unusual may be misinterpreted.
- **No time zone or reminders**: The bot stores due **text** only (e.g., "Friday 5pm"). It does not schedule real notifications.
- **Basic persistence**: Uses a local JSON file; if you redeploy elsewhere, the data won’t sync.
- **No multi-turn memory**: Each message is handled independently (outside of commands).

---

## Possible Improvements
- Normalize dates with `dateparser` or `duckling` to convert "Friday 5pm" → ISO timestamps.
- Add actual reminders via `apscheduler` or a server-side cron.
- Expand NER (custom SpaCy components) for priorities, people, locations.
- Add inline buttons for completing tasks.
- Swap JSON for a database (SQLite/Postgres) per user.

---

## Project Structure
```
quick-task-bot/
├─ bot.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ .gitignore
└─ tasks_store.json        # Created at runtime (persisted locally)
```

## .gitignore note
The `venv/` and `.env` are ignored so secrets and local environments are not committed.

---

## License
For educational use. Customize as needed.
